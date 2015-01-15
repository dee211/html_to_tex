# -*- coding: utf-8 -*-
from copy import copy
import os
from config import BaseConfig
from tag_configs import TagConfig, AddStylesTagConfig, \
    FixedWrapperTagConfig
from style_config import StyleConfig, FixedWrapperStyleConfig, BlockStyleConfig
from style_parameters_parser import OtherParametersParser, BackgroundColorParametersParser, \
    NumberParametersParser
from style_processors import ColorStyleProcessor, BaseStyleProcessor, \
    BackgroundColorBlockStyleProcessor, BackgroundColorTextStyleProcessor, FontSizeStyleProcessor
from tag_processors import ATagProcessor, BRTagProcessor, UlTagProcessor, \
    LiTagProcessor, OlTagProcessor, PTagProcessor, DivTagProcessor, TrTagProcessor, \
    TdTagProcessor, ThTagProcessor, TableTagProcessor, NoDisplayTagProcessor, TagProcessor, TextTagProcessor, \
    TBodyTagProcessor
from value_updaters import UniterMerger, ReplacerMerger

root_path = os.path.abspath(os.path.dirname(__file__))
HOME_DIR = '~/'
PROJECT_ROOT = root_path


class ConverterDefaultConfig(BaseConfig):
    tag_processors = {
        'text': TagConfig(TextTagProcessor),
        'a': TagConfig(ATagProcessor),
        'br': TagConfig(BRTagProcessor),
        'br /': TagConfig(BRTagProcessor),
        'br/': TagConfig(BRTagProcessor),
        'b': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold']
            },
        ),
        'strong': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold']
            },
        ),
        'other': TagConfig(TagProcessor),
        's': AddStylesTagConfig(
            additional_styles={
                'text-decoration': ['line-through']
            },
        ),
        'i': AddStylesTagConfig(
            additional_styles={
                'font-style': ['italic']
            },
        ),
        'h1': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold'],
                'font-size': ['20'],
                'newline': ['true'],
            }
        ),
        'h2': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold'],
                'font-size': ['16'],
                'newline': ['true'],
            }
        ),
        'h3': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold'],
                'font-size': ['13'],
                'newline': ['true'],
            }
        ),
        'h4': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold'],
                'font-size': ['10'],
                'newline': ['true'],
            }
        ),
        'h5': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold'],
                'font-size': ['7'],
                'newline': ['true'],
            }
        ),
        'h6': AddStylesTagConfig(
            additional_styles={
                'font-weight': ['bold'],
                'font-size': ['4'],
                'newline': ['true'],
            }
        ),
        'ul': TagConfig(UlTagProcessor),
        'li': TagConfig(LiTagProcessor),
        'ol': TagConfig(OlTagProcessor),
        'em': AddStylesTagConfig(
            additional_styles={
                'font-style': ['italic']
            },
        ),
        'sub': AddStylesTagConfig(
            additional_styles={
                'sub': ['true']
            },
        ),
        'sup': AddStylesTagConfig(
            additional_styles={
                'sup': ['true']
            },
        ),
        'p': TagConfig(PTagProcessor),
        'div': TagConfig(DivTagProcessor),
        'pre': AddStylesTagConfig(
            additional_styles={
                'preformatted': ['true']
            },
        ),
        'tr': TagConfig(TrTagProcessor),
        'td': TagConfig(TdTagProcessor),
        'th': TagConfig(ThTagProcessor),
        'table': TagConfig(TableTagProcessor),
        'tbody': TagConfig(TBodyTagProcessor),
        'script': TagConfig(NoDisplayTagProcessor),
        'style': TagConfig(NoDisplayTagProcessor),
        'head': TagConfig(NoDisplayTagProcessor),
    }
    block_style_processors = {
        'block-background-color': StyleConfig(cls=BackgroundColorBlockStyleProcessor),
        'border-width': BlockStyleConfig(parameter_name=u"linewidth"),
        "borderradius": BlockStyleConfig(parameter_name=u"roundcorner"),
        "margin-top": BlockStyleConfig(parameter_name=u"skipabove"),
        "margin-bottom": BlockStyleConfig(parameter_name=u"skipbelow"),
        "margin-left": BlockStyleConfig(parameter_name=u"leftmargin"),
        "margin-right": BlockStyleConfig(parameter_name=u"rightmargin"),
        "padding-top": BlockStyleConfig(parameter_name=u"innertopmargin"),
        "padding-bottom": BlockStyleConfig(parameter_name=u"innerbottommargin"),
        "padding-left": BlockStyleConfig(parameter_name=u"innerleftmargin"),
        "padding-right": BlockStyleConfig(parameter_name=u"innerrightmargin"),
    }
    text_style_processors = {
        'text-decoration': FixedWrapperStyleConfig(
            rules={
                u'line-through': (ur"\sout{", u"}"),
                u'underline': (u"\\underline{", u"}"),
                u'overline': (ur"$\overline{\text{", u"}}$")
            },
        ),
        'font-size': StyleConfig(FontSizeStyleProcessor),
        'other': StyleConfig(BaseStyleProcessor),
        'font-style': FixedWrapperStyleConfig(
            rules={
                u'italic': (ur"\textit{", u"}")
            }
        ),
        'font-weight': FixedWrapperStyleConfig(
            rules={
                u'bold': (ur"\textbf{", u"}")
            }
        ),
        'sub': FixedWrapperStyleConfig(
            rules={
                u"any": (ur"$_{\text{", u"}}$")
            }
        ),
        'sup': FixedWrapperStyleConfig(
            rules={
                u"any": (ur"$^{\text{", u"}}$")
            }
        ),
        'color': StyleConfig(ColorStyleProcessor),
        'text-background-color': StyleConfig(BackgroundColorTextStyleProcessor),
    }
    value_updaters = {
        u'text-decoration': UniterMerger(),
        u"text-color": ReplacerMerger(),
        u'font-size': ReplacerMerger(),
        u'other': ReplacerMerger(),
        u'font-style': ReplacerMerger(),
        u'font-weight': ReplacerMerger(),
        u'sub': ReplacerMerger(),
        u'sup': ReplacerMerger(),
        u'color': ReplacerMerger(),
        u'text-background-color': ReplacerMerger(),
        u'block-background-color': ReplacerMerger(),
        u'border-width': ReplacerMerger(),
        u"border-radius": ReplacerMerger(),
        u"margin-top": ReplacerMerger(),
        u"margin-bottom": ReplacerMerger(),
        u"margin-left": ReplacerMerger(),
        u"margin-right": ReplacerMerger(),
        u"padding-top": ReplacerMerger(),
        u"padding-bottom": ReplacerMerger(),
        u"padding-left": ReplacerMerger(),
        u"padding-right": ReplacerMerger(),
    }
    parameters_parsers = {
        'other': OtherParametersParser(),
        'background-color': BackgroundColorParametersParser(),
        'color': BackgroundColorParametersParser(),
        'width': NumberParametersParser(),
        'height': NumberParametersParser(),
        'border': NumberParametersParser(),
        'border-width': NumberParametersParser(),
        'margin-top': NumberParametersParser(),
        'margin-bottom': NumberParametersParser(),
        'margin-left': NumberParametersParser(),
        'margin-right': NumberParametersParser(),
        'padding-top': NumberParametersParser(),
        'padding-bottom': NumberParametersParser(),
        'padding-left': NumberParametersParser(),
        'padding-right': NumberParametersParser(),
        'font-size': NumberParametersParser(),
    }


class ConverterSafeConfig(ConverterDefaultConfig):
    tag_processors = copy(ConverterDefaultConfig.tag_processors)
    tag_processors.update({
        'li': FixedWrapperTagConfig(
            begin=ur"\item\parbox[t]{\linegoal}{",
            end=u"}",
        ),
        'p': FixedWrapperTagConfig(
            begin=ur"\leavevmode\\ \phantom{a} \leavevmode\\",
            end=u"",
        ),
        'div': FixedWrapperTagConfig(
            begin=ur"\leavevmode\\",
            end=u"",
        ),
    })


class ConverterSafestConfig(ConverterDefaultConfig):
    tag_processors = {
        'br': TagConfig(BRTagProcessor),
        'br /': TagConfig(BRTagProcessor),
        'br/': TagConfig(BRTagProcessor),
        'other': TagConfig(cls=TagProcessor),
        'script': TagConfig(NoDisplayTagProcessor),
        'style': TagConfig(NoDisplayTagProcessor),
        'div': FixedWrapperTagConfig(
            begin=ur"\leavevmode\\",
            end=u""
        ),
        'p': FixedWrapperTagConfig(
            begin=ur"\leavevmode\\ \phantom{a} \leavevmode\\",
            end=u"",
        ),
        'pre': AddStylesTagConfig(
            additional_styles={
                'preformatted': ['true']
            },
        ),
        'text': TagConfig(TextTagProcessor)
    }
    block_style_processors = {}
    text_style_processors = {}
