
class UserPagesRememberService:
    # chatId: pageNumber
    usersCurrentPage = dict()

    @staticmethod
    def NextPageInvoked(chatId):
        currentUserPage = UserPagesRememberService.usersCurrentPage.get(chatId)

        if currentUserPage is None:
            currentUserPage = 1
            UserPagesRememberService.usersCurrentPage[chatId] = currentUserPage
        nextPage = currentUserPage + 1
        UserPagesRememberService.usersCurrentPage[chatId] = nextPage

        return nextPage


    @staticmethod
    def BackPageInvoked(chatId):
        currentUserPage = UserPagesRememberService.usersCurrentPage.get(chatId)

        if currentUserPage is None:
            currentUserPage = 1
            UserPagesRememberService.usersCurrentPage[chatId] = currentUserPage
        nextPage = currentUserPage - 1
        UserPagesRememberService.usersCurrentPage[chatId] = nextPage

        return nextPage