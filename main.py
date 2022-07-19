import re


class CalcIPv4:
    def __init__(self, ip, cidr=None, mask=None):
        self.ip = ip
        self.cidr = cidr
        self.mask = mask

        self._set_broadcast()
        self._set_network()

    # GETTERS ###############################################
    @property
    def broadcast(self):
        return self._broadcast

    @property
    def network(self):
        return self._network

    @property
    def numb_ips(self):
        return self._get_number_ips()

    @property
    def numb_usable_ips(self):
        return self._get_number_usable_ips()

    @property
    def ip(self):
        return self._ip

    @property
    def cidr(self):
        return self._cidr

    @property
    def mask(self):
        return self._mask
    # END GETTERS ###############################################

    # SETTERS ###############################################
    @ip.setter
    def ip(self, value):
        if not self._valida_ip(value):
            raise ValueError('Invalid IP.')
        self._ip = value
        self._ip_bin = self._ip_to_bin(value)

    @cidr.setter
    def cidr(self, value):
        if not value:
            return
        if not isinstance(value, int):
            raise TypeError('Cidr need to be a Integer.')
        if value > 32:
            raise TypeError('Cidr must have 32 bits.')
        self._cidr = value
        self._bi_mask = (value * '1').ljust(32, '0')
        if not hasattr(self, 'mask'):
            self.mask = self._bin_to_ip(self._bi_mask)

    @mask.setter
    def mask(self, value):
        if not value:
            return
        if not self._valida_ip(value):
            raise ValueError('Invalid IP Mask.')
        self._mask = value
        self._bi_mask = self._ip_to_bin(value)

        if not hasattr(self, 'cidr'):
            self.cidr = self._bi_mask.count('1')
    # END SETTERS ###############################################

    @staticmethod
    def _valida_ip(ip):
        regexp = re.compile(
            r'^(\d{1,3}).(\d{1,3}).(\d{1,3}).(\d{1,3})$'
        )
        if regexp.search(ip):
            return True

    @staticmethod
    def _ip_to_bin(ip):
        block = ip.split('.')
        bi_block = [bin(int(x))[2:].zfill(8) for x in block]
        return ''.join(bi_block)

    @staticmethod
    def _bin_to_ip(ip):
        n = 8
        blocks = [str(int(ip[x:n+x], 2)) for x in range(0, 32, n)]
        return '.'.join(blocks)

    def _set_broadcast(self):
        host_bits = 32 - self.cidr
        self._broadcast_bin = self._ip_bin[:self.cidr] + (host_bits * '1')
        self._broadcast = self._bin_to_ip(self._broadcast_bin)
        return self._broadcast

    def _set_network(self):
        host_bits = 32 - self.cidr
        self._network_bin = self._ip_bin[:self.cidr] + (host_bits * '0')
        self._network = self._bin_to_ip(self._network_bin)
        return self._broadcast

    def _get_number_ips(self):
        return 2 ** (32 - self.cidr)

    def _get_number_usable_ips(self):
        return self.numb_ips - 2


if __name__ == '__main__':

    # Test IPs obtained randomly online.
    # You may use either the CIDR notation or the Mask, IPs are required.

    calc_ipva4_test1 = CalcIPv4(ip='131.91.79.243', cidr=24)
    print(f'IP: { calc_ipva4_test1.ip}')
    print(f'Mask: { calc_ipva4_test1.mask}')
    print(f'Network: { calc_ipva4_test1.network}')
    print(f'Broadcast: { calc_ipva4_test1.broadcast}')
    print(f'Cidr: { calc_ipva4_test1.cidr}')
    print(f'Total of IPs: { calc_ipva4_test1.numb_ips}')
    print(f'Total of usable IPs: { calc_ipva4_test1.numb_usable_ips}')

    print('\n'+'#'*80+'\n')

    calc_ipva4_test2 = CalcIPv4(ip='37.158.209.154', mask='255.255.255.128')
    print(f'IP: {calc_ipva4_test2.ip}')
    print(f'Mask: {calc_ipva4_test2.mask}')
    print(f'Network: {calc_ipva4_test2.network}')
    print(f'Broadcast: {calc_ipva4_test2.broadcast}')
    print(f'Cidr: {calc_ipva4_test2.cidr}')
    print(f'Total of IPs: {calc_ipva4_test2.numb_ips}')
    print(f'Total of usable IPs: {calc_ipva4_test2.numb_usable_ips}')
