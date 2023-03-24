import credential_app
import time
import os



def main():

    for i in range(100):
        #time.sleep(15)
        print("running {}".format(i))
        credential_app.main()
        time.sleep(15)


main()
