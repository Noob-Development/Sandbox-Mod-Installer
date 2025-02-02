from interface.location import *
from loggingConfig import setupLogging

logger = setupLogging()

if __name__ == '__main__':
    try:
        logger.info('Welcome to the Sandbox Mod Installer')
        logger.info('Please follow the instructions on screen to continue!"')
        logger.info('======================================================')

        app = wx.App()
        frame = DirSelector(None)
        frame.Show(True)
        app.MainLoop()

    except Exception as e:
        logger.critical(f'{e}')
        input("Press enter to exit...")
