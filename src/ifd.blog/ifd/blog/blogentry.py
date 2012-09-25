from five import grok
from plone.directives import dexterity, form
from zope import schema
from plone.namedfile.interfaces import IImageScaleTraversable

from plone.app.textfield import RichText
try:
    from plone.app.discussion.interfaces import IConversation
    USE_PAD = True
except ImportError:
    USE_PAD = False
from ifd.blog import MessageFactory as _


class IBlogEntry(form.Schema, IImageScaleTraversable):
    """
    A single blogentry that can contain images
    """
    text = RichText(
        title=_(u"Blog Entry"),
        description=_(u"Please enter main body text for this blog entry"),
        required=False,
    )
    allow_discussion = schema.Bool(
        title=_(u"Allow discussion on this item?"),
        default=True,
    )


class BlogEntry(dexterity.Container):
    grok.implements(IBlogEntry)


class View(grok.View):
    grok.context(IBlogEntry)
    grok.require('zope2.View')
    grok.name('view')

    def commentsEnabled(self, ob):
        if USE_PAD:
            conversation = IConversation(ob)
            return conversation.enabled()
        else:
            return self.portal_discussion.isDiscussionAllowedFor(ob)

    def commentCount(self, ob):
        if USE_PAD:
            conversation = IConversation(ob)
            return len(conversation)
        else:
            discussion = self.portal_discussion.getDiscussionFor(ob)
            return discussion.replyCount(ob)
