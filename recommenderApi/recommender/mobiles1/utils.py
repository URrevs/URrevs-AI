from recommenderApi.imports import dt
from recommender.mobiles1.extract import ExtractFeatures

def get_os(os_sen: str):
    os_sen = str(os_sen).lower()
    for os in ['ios', 'windows', 'firefox', 'amazon', 'blackberry', 'harmonyos', 'sailfish', 
            'symbian', 'tablet', 'meego', 'limo', 'bada', 'tizen', 'proprietary']:
        if os in os_sen:
            return os
    for os in ['symbian', 'nokia']:
        if os in os_sen:
            return 'nokia'
    for os in ['android', 'ophone']:
        if os in os_sen:
            return 'android'
    return 'another_os'

def get_network(network_sen: str):
    network_sen = str(network_sen).lower().replace(' ', '')
    if 'gsm' == network_sen: return 'gsm'
    for network in ['gsm/hspa/lte/5g', 'gsm/hspa/lte', 'gsm/cdma/hspa/evdo/lte/5g', 'gsm/lte',
        'gsm/cdma/hspa/evdo/lte', 'gsm/cdma/hspa/evdo', 'gsm/umts/hspa', 'gsm/cdma/hspa/lte/5g',
        'gsm/cdma/hspa/lte', 'gsm/cdma/hspa/cdma2000/lte/5g', 'gsm/cdma/hspa/cdma2000/lte', 
        'gsm/hspa/evdo/lte', 'gsm/hspa/evdo', 'gsm/umts', 'cdma/evdo/lte', 'gsm/cdma/evdo', 'cdma/evdo', 
        'cdma/hspa/evdo/lte', 'gsm/hspa']:
        if network in network_sen:
            return network
    return 'another_network'

def number(num: str):
    flag = True
    for char in num:
        if not(char.isdigit() or char == '.'):
            flag = False
            break
    if flag: return float(num)
    if 'x' in num:
        nums = num.split('x')
        return float(nums[0]) * float(nums[1])
    return 0

def get_cpu(cpu_sen: str):
    cpu_sen = str(cpu_sen).lower().replace('(', '').replace(')', '')
    result = 0
    if 'ghz' in cpu_sen:
        nums = cpu_sen.split('ghz')
        for num in nums[:-1]:
            try: result += number(num.split(' ')[-2]) * 1000
            except: pass
    elif 'mhz' in cpu_sen:
        nums = cpu_sen.split('mhz')
        for num in nums[:-1]:
            try: result += number(num.split(' ')[-2])
            except: pass
    return result, cpu_sen

def get_usb_type(usbType_sen: str):
    usbType_sen = str(usbType_sen).lower().replace(' ', '')
    if 'usb' == usbType_sen: return 'usb'
    for usb_type in ['miniusb', 'microusb', 'usbtype-c', 'proprietary', 'pop-port']:
        if usb_type in usbType_sen:
            return usb_type
    return 'another_usb_type'

def get_screen_type(screen_type_sen: str):
    screen_type_sen = str(screen_type_sen).lower()
    for screen_type in ['tft resistive touchscreen', 'tft lcd', 'tn tft', 'tft', 'super amoled+', 
        'igzo ips lcd', 'retina ips lcd', 'super retina oled', 'super retina xdr oled', 'super ips+ lcd', 
        'ips+ lcd', 'super ips+', 'super ips lcd2', 'led-backlit ips lcd', 'p-oled', 'ltpo amoled', 
        'ips-neo lcd', 'foldable oled', '3d lcd', 'super lcd3', 'true hd-ips lcd', 'hd-ips lcd', 
        'ips plus lcd', 'optic amoled', 'fluid amoled', 'super amoled plus', 'amoled resistive touchscreen', 
        'foldable dynamic amoled', 'dynamic amoled 2x', 'dynamic amoled', 'led-backlit lcd', 
        'sapphire crystal glass']:
        if screen_type in screen_type_sen:
            return screen_type
    for screen_type in ['amoled', 'lcd', 'tn']:
        if screen_type == screen_type_sen:
            return screen_type
    for screen_type in ['pls lcd', 'pls']:
        if screen_type in screen_type_sen:
            return 'pls lcd'
    for screen_type in ['super ips lcd', 's-ips lcd']:
        if screen_type in screen_type_sen:
            return 'super ips lcd'
    for screen_type in ['super clear lcd', 'sc-lcd']:
        if screen_type in screen_type_sen:
            return 'super clear lcd'
    for screen_type in ['super lcd2', 's-lcd2']:
        if screen_type in screen_type_sen:
            return 'super lcd2'
    for screen_type in ['super lcd', 's-lcd']:
        if screen_type in screen_type_sen:
            return 'super lcd'
    for screen_type in ['ips lcd', 'ips fl lcd']:
        if screen_type in screen_type_sen:
            return 'ips lcd'
    if 'oled' in screen_type_sen: return 'super amoled'
    return 'another_screen_type'

# ['4GB 512MB RAM (SS)', '8GB 512MB RAM (DS)']
def get_mem_ram(mem_ram_sen: str):
    mem_ram_sen = str(mem_ram_sen).lower()
    varients = mem_ram_sen.split(',')
    varients[0] = varients[0].replace('[', '').replace("'", '').strip()
    varients[-1] = varients[-1].replace(']', '').replace("'", '').strip()
    new = [0 for _ in range(6)]
    for i in range(len(varients)):
        nums = varients[i].split(' ')
        count = 0
        for num in nums:
            num = num.replace('(', '').replace(')', '')
            if 'mb' in num:
                num = num.replace('mb', '').strip()
                try: new[2*i+count] = int(num)
                except: pass
                count += 1
            if 'gb' in num: 
                num = num.replace('gb', '').strip()
                try: new[2*i+count] = int(num) * 1024
                except: pass
                count += 1
            if count == 2: break
    return new

def get_cam(mainCam_sen: str):
    mainCam_sen = str(mainCam_sen).lower()
    cam_num = 0
    enum = {
        'single': 1, 'dual': 2, 'triple': 3, 'quad': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    for num in ['single', 'dual', 'triple', 'quad', 'five', 'six', 'seven', 'eight', 'nine', 'ten']:
        if num in mainCam_sen: 
            cam_num = enum[num]
            mainCam_sen = mainCam_sen.replace(num, '')
            break
    try: num = float(mainCam_sen.split('mp')[0].replace(',', '').replace(' ', ''))
    except: num = 0
    return cam_num, num

def dateAsInteger(date: dt) -> float:
        reference: dt = dt(1999, 1, 1)
        try:
            return (date - reference).total_seconds()
        except:
            print(f'"{date}" is not valid input')
            return 0

def date_convert(date: str):
    if date == '': out = '1999'
    else: out = date
    try: out = dt.strptime(out, '%Y, %B %d')
    except: 
        try: out = dt.strptime(out, '%Y, %B')
        except: 
            try: out = dt.strptime(out, '%Y')
            except: out = dt(1999, 1, 1)
    return ExtractFeatures().dateAsInteger(out)

