import secrets

def makeKey():
  keyName = "static.key"
  f = open(r"/home/studentas/Documents/python/OpenVPN_speed_test/config/" + keyName, "a")
  f.seek(0)
  f.truncate()

  try:
    f.write("#\n# 2048 bit OpenVPN static key\n#\n-----BEGIN OpenVPN Static key V1-----\n")
    for index in range(16):
      key = secrets.token_hex(16)
      f.write(key + "\n")
    f.write("-----END OpenVPN Static key V1-----")
    f.close()
  except Exception as e:
    print(e)