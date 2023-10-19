def copy_certificate(certFile):
    # opening both files in read only mode to read initial contents
    f1 = open(certFile, 'r')
    f2 = open("/usr/local/lib/python3.10/site-packages/certifi/cacert.pem", 'a+')

    # appending the contents of the second file to the first file
    f2.write(f1.read())

    # closing the files
    f1.close()
    f2.close()

copy_certificate("/app/ca.cert")