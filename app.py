import binascii
from google.protobuf.json_format import MessageToJson
from banner_pb2 import Garena_420
import requests
import json
import binascii
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_token_for_region(region):
    try:
        if region == "ind":
            uid = "3510149624"
            password = "3D45A8D95755FB8831FA413AC042BF642A21F12CE3E8DF7AB4E57AA6B21D7F86"
        elif region == "bd":
        	uid = "4184078684"
        	password = "BA8CA6525177CBC966CFBDBD3EA592D80836C55C654208B87EC81EF7726F36FC"
        elif region == "sg":
        	uid = "3510665680"
        	password = "931F932D3C8B85ACD41AA70080BD2155F256E0882042486FE952F0217451E417"
        elif region == "pk":
        	uid = "3510748984"
        	password = "FA6110AFBE251A762D468F5E46FBF3539E746C37884AF31E991FFFDC2D64C6B2"
        elif region == "na":
        	uid = "3510758518"
        	password = "5316049E2D8893205E1F99119361FE66662ED540DA7E9810A5845B448B8D3795"
        elif region == "br":
        	uid = "3512124815"
        	password = "DB6AD7608BCF9D7F9A796104DEAA1C591AD7522A01B12164908DC2DE06788C62"
        elif region == "eu":
        	uid = "3512141306"
        	password = "507324BE413D6AFDF117986336B1AFED625AE1537B04D6BBDDC744AEB6A48942"
        elif region == "me":
        	uid = "3512149672"
        	password = "527FEA196F134E9693242DA09657613314000A1F0ECD646CE7D52E9EAA15505C"
        elif region == "vn":
        	uid = "3512177839"
        	password = "62CDA90C47D5B8BFE13DB94A7DAA4BC6B28FFE2AB7ABE4DC1D991A7528679402"
        elif region == "th":
        	uid = "3512231653"
        	password = "73CD502588FC363D222DB8C29219D20DC5B76AC5562D5D90004865537999A78E"
        elif region == "sp":
        	uid = "3512231653"
        	password = "73CD502588FC363D222DB8C29219D20DC5B76AC5562D5D90004865537999A78E"
        elif region == "tw":
            uid = "3526534489"
            password = "AA7C8850D652996EF3DE6D9B1B2A6A0B67363632EC6EBA21DD9FA411B70193C3"
        elif region == "id":
            uid = "3526802295"
            password = "85223B8905AFF303C55F01F3AEA85F510C6D30CEA382822FDE542A6C2527A0F4"
        url = (f"https://jwt-generator-phi.vercel.app/get-token?uid={uid}&password={password}")
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            print(f"Failed to get token for {region}: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request for token failed: {e}")
        return None
        

def get(region):
    if region == "ind":
        url = "https://client.ind.freefiremobile.com/LoginGetSplash"
    elif region == "br":
        url = "https://client.us.freefiremobile.com/LoginGetSplash"
    else:
        url = "https://clientbp.ggblueshark.com/LoginGetSplash"
    body = bytes.fromhex("9223af2eab91b7a150d528f657731074")
    bearer = get_token_for_region(region)
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {bearer}",
        'Content-Type': "application/x-www-form-urlencoded",
        'Expect': "100-continue",
        'X-Unity-Version': "2018.4.11f1",
        'X-GA': "v1 1",
        'ReleaseVersion': "OB50"
    }

    response = requests.post(url, data=body, headers=headers)
    hex_string = response.content.hex()
    try:
        binary_data = bytes.fromhex(hex_string)
        root = Garena_420()
        root.ParseFromString(binary_data)
        json_output = MessageToJson(root)
        return json_output
        
    except binascii.Error as e:
        return("Error")
    except Exception as e:
        return("Error during parsing")
    

@app.route('/banner', methods=['GET'])
def banner_handle():
    region = request.args.get('region')
    main = get(region)
    return main
    
if __name__ == '__main__':
    app.run(debug=True)
    
