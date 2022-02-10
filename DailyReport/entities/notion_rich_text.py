"""Notion Database Rich_text Propertie Entities"""

from dataclasses import dataclass

from DailyReport.utils import DotDict


@dataclass
class RichText:
    def __init__(
            self,
            object: str,
            type: str,
            rich_text: dict
    ):
        self.object = object
        self.type = type
        self.rich_text = DotDict(rich_text)

"""
{
    'object': 'property_item', 
    'type': 'rich_text', 
    'rich_text': 
    {
        'type': 'text', 
        'text': 
        {
            'content': 'test !!!!', 
            'link': None
        }, 
        'annotations': 
        {
            'bold': False, 
            'italic': False, 
            'strikethrough': False, 
            'underline': False, 
            'code': False, 
            'color': 'default'
        }, 
        'plain_text': 'test !!!!', 
        'href': None
    }
}
"""