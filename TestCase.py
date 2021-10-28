
class TestCase:
    pageId = ''
    actions = []
    expected_result = ''

    def __init__(self, caseDict):
        print(caseDict)
        self.pageId = caseDict['pageId']
        actions = []
        actions_dict = caseDict['actions']
        for action_dict in actions_dict:
            actionTmp = Action(action_dict)
            actions.append(actionTmp)
        self.actions = actions


class Page:
    ID = '',
    title = '',
    route = '',
    def __init__(self, ID, title, route):
        self.ID = ID
        self.title = title
        self.route = route

class Element:
    type  = 'button',
    ID = '',
    pageId = '',
    element_content = '',
    icon  = '',
    x = 0,
    y = 0,
    w = 0,
    h = 0,
    def __init__(self, elementDict):
        self.type = elementDict['type']
        self.ID = elementDict['ID']
        self.element_content = elementDict['element_content']
        self.x = elementDict['x']
        self.y = elementDict['y']
        self.w = elementDict['w']
        self.h = elementDict['h']
    # def __init__(self, type, pageId, element_label, icon):
    #     self.type = type
    #     self.element_label = element_label
    #     self.icon = icon

class Action:
    actionType =  '' # click, dbclick
    element: Element
    def __init__(self, actionDict):
        self.actionType = actionDict['action']
        self.element = Element(actionDict['element'])
    # def __init__(self, actionType, element):
    #     self.actionType = actionType
    #     self.element = element

class TestResult:
    resultType = '' # number, text, route
    value = ''
    def __init__(self, result_type, ):
        self.resultType = result_type
        self.value = ''




#
# Action {
# 	element:  {
# 		type: 'button',
# 		pageId: '11111',
# 		element_label: 'Home',
# 		icon: '11111',
# 	},
# 	action: 'click',
# 	action_resp: 'route_next_page',
# 	expected_result:[],
# }
#
# Page: {
# 	ID: '',
# 	title: '',
# 	route: '',
# }


