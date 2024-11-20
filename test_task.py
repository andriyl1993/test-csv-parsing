import unittest
from unittest import mock
from task import main


persons_data = b"""chromosome,position,ref,alt
chr21,111395,A,C
chr4,177397,T,T
chr1,155302,G,T
chr9,104165,T,C
chr8,103905,G,A
chr8,112280,C,C
chr5,128657,A,G
chr4,130495,T,A
chr22,166237,G,C
chr18,178907,C,C
chr19,188341,A,A
"""

enrichment_data = b"""chromosome,position,ref,alt,info
chr18,178907,C,C,info_1
chr8,103905,G,A,info_2
chr21,111395,A,C,info_3
chr8,112280,C,A,info_4
chr15,170284,A,G,info_5
chr3,172357,C,C,info_6
chr19,125203,A,A,info_7
"""

class MockedResponse:
    def __init__(self, content):
        self._content = content

    @property
    def content(self):
        return self._content


class TestTask(unittest.TestCase):
    @mock.patch('requests.get')
    def test(self, mocked_get):
        mocked_get.side_effect = (
            MockedResponse(persons_data),
            MockedResponse(enrichment_data),
        )
        person_url = "url1"
        enrichment_url = "url2"
        result = main(person_url, enrichment_url)
        expected_result = 'chromosome,position,ref,alt,info\nchr21,111395,A,C,info_3\nchr4,177397,T,T,\nchr1,155302,G,T,\nchr9,104165,T,C,\nchr8,103905,G,A,info_2\nchr8,112280,C,C,\nchr5,128657,A,G,\nchr4,130495,T,A,\nchr22,166237,G,C,\nchr18,178907,C,C,info_1\nchr19,188341,A,A,\n'
        self.assertEqual(result, expected_result)