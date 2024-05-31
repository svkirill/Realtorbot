from Services.RealtorsService import RealtorsService

class UserPagesRememberService:
    # chatId: pageNumber
    usersCurrentPage = dict()

    # chatId: True/False
    usersGetInMainMenu = dict()

    @staticmethod
    def NextPageInvoked(chatId):
        UserPagesRememberService.CleanGetRealtorsList(chatId)

        currentUserPage = UserPagesRememberService.usersCurrentPage.get(chatId)

        if currentUserPage is None:
            currentUserPage = 1
            UserPagesRememberService.usersCurrentPage[chatId] = currentUserPage

        nextPage = currentUserPage + 1
        UserPagesRememberService.usersCurrentPage[chatId] = nextPage

        return nextPage

    @staticmethod
    def CleanGetRealtorsList(chatId):
        result = UserPagesRememberService.usersGetInMainMenu.get(chatId)

        if result:
            UserPagesRememberService.usersGetInMainMenu[chatId] = False

    @staticmethod
    def UserGetRealtorsList(chatId):
        UserPagesRememberService.usersCurrentPage[chatId] = True

    @staticmethod
    def GetCurrentUserPage(chatid):
        return UserPagesRememberService.usersCurrentPage.get(chatid)

    @staticmethod
    def BackPageInvoked(chatId):
        UserPagesRememberService.CleanGetRealtorsList(chatId)

        currentUserPage = UserPagesRememberService.usersCurrentPage.get(chatId)

        if currentUserPage is None:
            currentUserPage = 1
            UserPagesRememberService.usersCurrentPage[chatId] = currentUserPage
        nextPage = currentUserPage - 1
        UserPagesRememberService.usersCurrentPage[chatId] = nextPage

        return nextPage

    @staticmethod
    def CheckResendChangedPages(uniqueCode):
        chatIdsToResend = []

        # Реальная страница риэлтора (пока не знаем)
        realtorPage = None

        # Перебираем страницы всех пользователей, на которых они находятся
        for chatid, page in UserPagesRememberService.usersCurrentPage.items():
            # Если страница риэлтора еще не известна, то делаем проверку, может
            # он находится на странице пользователя, которого сейчас проверяем
            if realtorPage is None:
                page, contains = RealtorsService.CheckRealtorInPage(uniqueCode, page)

                # Если на проверяемой странице содержится риэлтор, то сохраняем ее,
                # чтобы больше не запускать поиск
                if contains:
                    realtorPage = page
            # Если страница с риэлтором соответствует странице пользователя, то добавляем
            # данного пользователя в список chatIdsToResend, в котором будут определены
            # пользователи, которым нужно переотправить меню.
            if page == realtorPage:
                chatIdsToResend.append(chatid)


        for chatid, isOnFirstPage in UserPagesRememberService.usersGetInMainMenu.items():
            if isOnFirstPage:
                if realtorPage is None:
                    page, contains = RealtorsService.CheckRealtorInPage(uniqueCode, 1)
                    if contains:
                        realtorPage = page

                if page == realtorPage:
                    chatIdsToResend.append(chatid)


        print(chatIdsToResend)
        return chatIdsToResend