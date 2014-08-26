from splinter import Browser
import string

class HackFreeRice:
    def __init__(self, browserType='chrome'):
        self.correct = 0
        self.incorrect = 0

        self.readCredentials()

        # Initialize splinter (other possible values include 'phantomjs' and 'firefox')
        self.browser = Browser(browserType)

    def initialize(self, verbose=False):
        # Initialize until it is successful
        while True:
            if self.tryInitialize():
                if verbose:
                    print 'Successfully initialized.'
                break

    def readCredentials(self, verbose=False):
        # Read credentials from file
        with open('config') as f:
            username, password = f.readlines()
            self.username = username.strip()
            self.password = password.strip()

        if verbose:
            print 'Your username is %s' % self.username
            print 'Your password is %s' % self.password

    def tryInitialize(self, verbose=False):
        # Open freerice
        self.browser.visit('http://freerice.com/user/login')

        # Close pop-up, if present
        if self.browser.is_element_present_by_id('wfp-ew-dialog-close'):
            if self.browser.find_by_id('wfp-ew-dialog-close').first.visible:
                # Closed popup if present and visible
                self.browser.find_by_id('wfp-ew-dialog-close').click()

        # Login
        self.browser.execute_script("$('#edit-name').val('%s')" % self.username)
        self.browser.execute_script("$('#edit-pass').val('%s')" % self.password)
        self.browser.execute_script("$('#edit-submit').click()")

        already_logged_in = self.browser.is_text_present('Logout')
        login_check_string = '%s has earned' % self.username
        successful_login = self.browser.is_text_present(login_check_string)
        if already_logged_in or successful_login:
            if verbose:
                print 'Successfully logged in!'
        else:
            if verbose:
                print 'Login failed.'
            return False

        # Change subject to math
        self.browser.execute_script("window.location.href = 'http://freerice.com/frapi/category_selected/18492'")

        if self.browser.is_text_present('Multiplication Table'):
            if verbose:
                print 'Successfully navigated to Multiplication Table'
            return True
        else:
            return False

    def doQuestion(self, verbose=False):

        # Close twitter solicitation, if present
        self.browser.execute_script("$('#twt-skip').click()")

        question_text = self.browser.evaluate_script("$('#question-title').text()")
        question_text = question_text.split('loader')
        question_text = ''.join(question_text)
        if verbose:
            print 'The question is: %s' % question_text

        question_text = string.replace(question_text, ' x ', '*').strip()
        if verbose:
            print 'The code representation of the question is: %s' % question_text

        question_answer = self.browser.evaluate_script(question_text)
        if verbose:
            print 'The answer is: %s' % question_answer

        add_id_script = "$('a:contains(\"%s\").answer-item').attr('id', 'clickthisone')" % question_answer
        if verbose:
            print 'Script to add id is:', add_id_script
        self.browser.execute_script(add_id_script)
        self.browser.find_by_id('clickthisone').click()

        if self.browser.is_text_present('Correct!'):
            print 'Got the answer right. Yeah!'
            self.correct += 1
        else:
            print 'Oops. Got that one wrong.'
            self.incorrect += 1

        print 'You have donated %s grains of rice!' % str(10 * self.correct)

if __name__ == "__main__":
    hackfreerice = HackFreeRice()
    while True:
        try:
            hackfreerice.doQuestion()
        except:
            hackfreerice.initialize()
