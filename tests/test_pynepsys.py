import unittest
from pynepsys import Apex


class PyNepSysTest(unittest.TestCase):
    def test_xml_parsing(self):
        test_xml = """<status software="4.53_4D19" hardware="1.0">
    <hostname>apex</hostname>
    <serial>AC4:12345</serial>
    <timezone>-7.00</timezone>
    <date>04/17/2020 20:31:22</date>
    <power>
        <failed>04/17/2020 19:49:45</failed>
        <restored>none</restored>
    </power>
    <probes>
        <probe>
            <name>Temp</name>
            <value>75.5 </value>
            <type>Temp</type>
        </probe>
        <probe>
            <name>pH</name>
            <value>8.49 </value>
            <type>pH</type>
        </probe>
        <probe>
            <name>ORP</name>
            <value>   316 </value>
            <type>ORP</type>
        </probe>
        <probe>
            <name>FLx11_3</name>
            <value> 0.0 </value>
        </probe>
    </probes>
    <outlets>
        <outlet>
            <name>VarWhiteLED</name>
            <outputID>0</outputID>
            <state>RD120W</state>
            <deviceID>base_Var1</deviceID>
        </outlet>
        <outlet>
            <name>Vortech_East</name>
            <outputID>75</outputID>
            <state>TBL</state>
            <deviceID>12_1</deviceID>
            <xstatus>OK</xstatus>
        </outlet>
        <outlet>
            <name>VarSpd4_13_4</name>
            <outputID>71</outputID>
            <state>RD120W</state>
            <deviceID>13_4</deviceID>
        </outlet>
        <outlet>
            <name>18_1</name>
            <outputID>95</outputID>
            <state>AOF</state>
            <deviceID>18_1</deviceID>
        </outlet>
        <outlet>
            <name>18_2</name>
            <outputID>96</outputID>
            <state>AON</state>
            <deviceID>18_2</deviceID>
        </outlet>
        <outlet>
            <name>18_3</name>
            <outputID>96</outputID>
            <state>ON</state>
            <deviceID>18_3</deviceID>
        </outlet>
        <outlet>
            <name>18_4</name>
            <outputID>97</outputID>
            <state>OFF</state>
            <deviceID>18_4</deviceID>
        </outlet>
    </outlets>
</status>"""
        apex = Apex('127.0.0.1')
        apex._parse_xml_state(test_xml)

        self.assertEqual(apex.hostname, 'apex')
        self.assertEqual(apex.serial, 'AC4:12345')
        # outlets
        self.assertEqual(apex.outlets.__len__(), 7)
        outlet = apex.outlets['VarWhiteLED']
        self.assertEqual(outlet.device_id, 'base_Var1')
        self.assertEqual(outlet.state, 'RD120W')
        self.assertFalse(outlet.is_off())
        self.assertTrue(outlet.is_on())
        self.assertFalse(outlet.is_auto())
        outlet = apex.outlets['Vortech_East']
        self.assertEqual(outlet.state, 'TBL')
        self.assertTrue(outlet.is_on())
        outlet = apex.outlets['18_1']
        self.assertEqual(outlet.device_id, '18_1')
        self.assertEqual(outlet.output_id, '95')
        self.assertTrue(outlet.is_off())
        self.assertFalse(outlet.is_on())
        self.assertTrue(outlet.is_auto())
        outlet = apex.outlets['18_2']
        self.assertFalse(outlet.is_off())
        self.assertTrue(outlet.is_on())
        self.assertTrue(outlet.is_auto())
        outlet = apex.outlets['18_3']
        self.assertFalse(outlet.is_off())
        self.assertTrue(outlet.is_on())
        self.assertFalse(outlet.is_auto())
        outlet = apex.outlets['18_4']
        self.assertTrue(outlet.is_off())
        self.assertFalse(outlet.is_on())
        self.assertFalse(outlet.is_auto())

        # probes
        self.assertEqual(apex.probes.__len__(), 4)
        probe = apex.probes['Temp']
        self.assertEqual(probe.value, 75.5)
        self.assertEqual(probe.type, 'Temp')
        probe = apex.probes['FLx11_3']
        self.assertEqual(probe.value, 0)
        self.assertIsNone(probe.type)


if __name__ == '__main__':
    unittest.main()
