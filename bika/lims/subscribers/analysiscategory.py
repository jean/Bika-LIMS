from DateTime import DateTime
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from bika.lims import bikaMessageFactory as _
import transaction

def ActionSucceededEventHandler(category, event):

    wf = getToolByName(category, 'portal_workflow')
    pc = getToolByName(category, 'portal_catalog')
    rc = getToolByName(category, 'reference_catalog')
    pu = getToolByName(category, 'plone_utils')

    if event.action == "deactivate":
        # A category cannot be deactivated if it contains services
        ars = pc(portal_type='AnalysisService', getCategoryUID = category.UID())
        if ars:
            message = _("Category cannot be deactivated because it contains Analysis Services")
            pu.addPortalMessage(message, 'error')
            transaction.get().abort()
            raise WorkflowException
