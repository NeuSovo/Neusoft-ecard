from band.apps import OrderStatusConfig as OSC


class UpdateStatusError(Exception):
    def __init__(self, oldst, st, issue_user=None):
        self.issue_user = issue_user
        self.oldst = OSC.CodeToName(oldst)
        self.st = OSC.CodeToName(st)

    def __str__(self):
        info = 'Status: "{oldst}" to Status: "{st}" is Invalid'.format(
            oldst=self.oldst, st=self.st)
        if self.issue_user:
            info = info + \
                '\nissue_user "{issue_user}" Error '.format(
                    issue_user=self.issue_user)

        return info


class issueUserError(UpdateStatusError):
    pass
