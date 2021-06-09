from django.db.models import Manager, QuerySet, Q
import ipaddress


class IPLookupQuerySet(QuerySet):

    def ip_lookup(self, ip_address):
        return self.filter(Q(network__supernets=ip_address) | Q(ip_address=ipaddress.ip_address(ip_address)))


class IPLookupManager(Manager):

    def get_queryset(self):
        return IPLookupQuerySet(self.model, using=self._db)

    def ip_lookup(self, ip_address):
        return self.get_queryset().ip_lookup(ip_address)
