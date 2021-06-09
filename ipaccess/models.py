from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .core.models import IpAddressField, IpNetworkField
from .managers import IPLookupManager


class BlockIPAddress(models.Model):
    network = IpNetworkField(null=True, default='127.0.0.0/32', verbose_name=_('IP Network mask'))
    ip_address = IpAddressField(null=True, verbose_name=_('Individual IP address'))
    reason_for_block = models.TextField(blank=True, null=True, help_text=_("Optional reason for block"))
    is_enabled = models.BooleanField(default=True,help_text=_('Rule enabled true/false'))

    objects = IPLookupManager()

    def __str__(self):
        if self.network:
            return 'Network mask : %s' % self.network
        else:
            return 'IP address : %s ' % self.ip_address

    class Meta:
        db_table = 'ip_access_rules'
        verbose_name = _('IPs & masks rules')
        verbose_name_plural = _('IPs & masks rules')

    def clean(self):
        if not self.network and not self.ip_address:
            raise ValidationError({'ip_address':_('Network Mask and IP address both cannot be blank')})