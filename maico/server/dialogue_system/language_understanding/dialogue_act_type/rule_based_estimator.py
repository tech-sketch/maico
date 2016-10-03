# -*- coding: utf-8 -*-


class RuleBasedDialogueActTypeEstimator(object):
    def __init__(self):
        pass

    def estimate(self, attribute):
        if attribute['small_area']:
            return 'RespondSmallArea'
        elif attribute['middle_area']:
            return 'RespondMiddleArea'
        elif attribute['large_area']:
            return 'RespondLargeArea'
        elif attribute['date']:
            return 'RespondSchedule'
        elif attribute['seamt']:
            return 'RespondSeaMt'
        else:
            return 'OTHER'
