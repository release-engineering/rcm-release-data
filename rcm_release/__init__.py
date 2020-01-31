#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from optparse import OptionParser

import pdc_client
import beanbag
import six
import requests

DEFAULT_PDC_INSTANCE = 'https://pdc.engineering.redhat.com/rest_api/v1/'


class GenericReleaseDataBackend(six.with_metaclass(ABCMeta)):
    backend = "generic"

    def __init__(self, backend=None):  # TODO: add backend argument
        pass

    @abstractmethod
    def content_delivery_repos(self):
        """
        Args:
            release - expects release in format rhel-7.6 or supp-7.6@rhel-7
        Returns

                [
                  {
                    "shadow":           bool,
                    "release_id":       string,
                    "variant_uid":      string,
                    "arch":             string,
                    "service":          string,
                    "repo_family":      string,
                    "content_format":   string,
                    "content_category": string,
                    "name":             string,
                    "product_id":       int
                  },
                  ...
                ]

        """
        raise NotImplementedError

    @abstractmethod
    def release_variants(self):
        """
        "arches": [
            "string"
        ],
        "id": "string",
        "name": "string",
        "release": "Release.release_id",
        "type": "VariantType.name",
        "uid": "string",
        "variant_release (optional, default=null, nullable)": "string",
        "variant_version (optional, default=null, nullable)": "string"
    }
    """
        raise NotImplementedError


class Pdc(GenericReleaseDataBackend, pdc_client.PDCClient):
    def __init__(self, pdc):
        # super(self, GenericReleaseDataBackend).__init__('pdc') # Test, TODO delete
        pdc_client.PDCClient.__init__(self, pdc)
        self.session = requests.Session()
        self.session.auth = beanbag.KerbAuth()

    def get_session(self, url_postfix):
        api_url = DEFAULT_PDC_INSTANCE + url_postfix
        pdc_instance = beanbag.BeanBag(api_url, session=self.session)
        return pdc_instance

    def content_delivery_repos(self):
        return self.__get_all("content-delivery-repos/")

    def release_variants(self):
        return self.__get_all("release-variants/")

    def __get_all(self, name):
        all_pages = []
        session = self.get_session(name)
        all_pages.append(session())  # to get first page
        i = 2
        while 'next' in all_pages[-1].keys() and all_pages[-1]['next']:
            all_pages.append(session(page=i))
            i += 1
            print(all_pages[-1])
        return all_pages