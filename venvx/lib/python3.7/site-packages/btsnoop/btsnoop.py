import os
from dataclasses import dataclass
import dataclasses
import numpy as np
from numpy import uint8, uint16, uint32, int8, int16, int32
from bitstring import BitArray
from binascii import hexlify
import inspect
from enum import IntEnum, IntFlag
import encodings

class lmp_version(IntEnum):
   V1_0b = 0
   V1_1 = 1
   V2_0b = 2
   V2_0_EDR = 3
   V2_1_EDR = 4
   V3_0_HS = 5
   V4_0 = 6
   V4_1 = 7
   V4_2 = 8
   V5_0 = 9

   def __str__(self):
        for x in lmp_version.__members__:
            if lmp_version.__members__[x] == self:
                return x
        return 'unknown'

class lmp_manufacture(IntEnum):
    Ericsson = 0
    Nokia = 1
    Intel_Corp = 2
    IBM = 3
    Toshiba_Corp = 4
    _3COM = 5
    Microsoft = 6
    Lucent = 7
    Motorola = 8
    Infineon = 9
    Qualcomm_CSR = 10
    Silicon_Wave = 11
    Digianswer = 12
    Texas_Instruments = 13
    Parthus = 14
    Broadcom_Corporation = 15
    Qualcomm = 29 
    Renesas = 54
    MediaTek = 70
    Marvell = 72
    Apple = 76
    Harman = 87
    Nordic = 89
    Realtek = 93
    RDA = 97
    MindTree = 106
    ShangHai_Super_Smart = 114
    Vimicro = 129
    Quintic = 142
    Airoha = 148
    Bestechnic = 688

    def __str__(self):
        for x in lmp_manufacture.__members__:
            if lmp_manufacture.__members__[x] == self:
                return x
        return 'unknown'       
        
class uint16_be(uint16):
    pass
    
class uint32_be(uint32):
    pass

class UINT16_BE(uint16):    
    def __repr__(self):
        self.repr = '0x{:04x}'.format(self)
        return self.repr

class UINT32_BE(uint32):    
    def __repr__(self):
        self.repr = '0x{:08x}'.format(self)
        return self.repr
        
class UINT8(uint8):
    def __repr__(self):
        self.repr = '0x{:02x}'.format(self)
        return self.repr
        
class UINT16(uint16):
    def __repr__(self):
        self.repr = '0x{:04x}'.format(self)
        return self.repr

    def __str__(self):
        return '0x{:04x}'.format(self)   

class UINT32(uint32):
    def __repr__(self):
        self.repr = '0x{:08x}'.format(self)
        return self.repr

class bdaddr_t(bytearray):
    itemsize = 6
    def __repr__(self):
        self.repr = '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(self[5],self[4],self[3],self[2],self[1],self[0])
        return self.repr

    def __str__(self):
        return '{:02X}:{:02X}:{:02X}:{:02X}:{:02X}:{:02X}'.format(self[5],self[4],self[3],self[2],self[1],self[0])
        
class attribute_id_t(IntEnum):
    itemsize = 2

    SERVICE_RECORD_HANDLE = 0x0000
    SERVICE_CLASS_ID = 0x0001
    SERVICE_RECORD_STATE = 0x0002
    SERVICE_ID = 0x0003 # useful if service is described in more than one SDP server
    PROTOCOL_DESC_LIST = 0x0004
    ADDITIONAL_PROTOCOL_DESC_LIST = 0x000D
    BROWSE_GROUP_LIST = 0x0005 # usually is PublicBrowseRoot (0x1002)
    LANGUAGE_BASE_ATTRIBUTE_ID_LIST = 0x0006
    SERVICE_INFO_TTL = 0x0007
    SERVICE_AVAILABILITY = 0x0008
    PROFILE_DESC_LIST = 0x0009
    DOC_URL = 0x000A
    CLIENT_EXE_URL = 0x000B
    ICON_URL = 0x000C
    #SERVICE_NAME = 0x0000 + LANGUAGE_BASE_ATTRIBUTE_ID_LIST
    #SERVICE_DESC = 0x0001 + 
    #PROVIDER_NAME = 0x0002 + 

class service_class_t(IntEnum):
    ServiceDiscoveryServerServiceClassID = 0x1000
    BrowseGroupDescriptorServiceClassID = 0x1001
    SerialPort = 0x1101
    LANAccessUsingPPP = 0x1102
    DialupNetworking = 0x1103
    IrMCSync = 0x1104
    OBEXObjectPush = 0x1105
    OBEXFileTransfer = 0x1106
    IrMCSyncCommand = 0x1107
    Headset = 0x1108
    CordlessTelephony = 0x1109
    AudioSource = 0x110A
    AudioSink = 0x110B
    AV_RemoteControlTarget = 0x110C
    AdvancedAudioDistribution = 0x110D
    AV_RemoteControl = 0x110E
    AV_RemoteControlController = 0x110F
    Intercom = 0x1110
    Fax = 0x1111
    Headset_AG = 0x1112
    WAP = 0x1113
    WAP_CLIENT = 0x1114
    PANU = 0x1115
    NAP = 0x1116
    GN = 0x1117
    DirectPrinting = 0x1118
    ReferencePrinting = 0x1119
    Basic_Imaging_Profile = 0x111A
    ImagingResponder = 0x111B
    ImagingAutomaticArchive = 0x111C
    ImagingReferencedObjects = 0x111D
    Handsfree = 0x111E
    HandsfreeAudioGateway = 0x111F
    DirectPrintingReferenceObjectsService = 0x1120
    ReflectedUI = 0x1121
    BasicPrinting = 0x1122
    PrintingStatus = 0x1123
    HumanInterfaceDeviceService = 0x1124
    HardcopyCableReplacement = 0x1125
    HCR_Print = 0x1126
    HCR_Scan = 0x1127
    Common_ISDN_Access = 0x1128
    SIM_Access = 0x112D
    Phonebook_Access_PCE = 0x112E
    Phonebook_Access_PSE = 0x112F
    Phonebook_Access = 0x1130
    Headset_HS = 0x1131
    Message_Access_Server = 0x1132
    Message_Notification_Server = 0x1133
    Message_Access_Profile = 0x1134
    GNSS = 0x1135
    GNSS_Server = 0x1136
    _3D_Display = 0x1137
    _3D_Glasses = 0x1138
    _3D_Synchronization = 0x1139
    MPS_Profile_UUID = 0x113A
    MPS_SC_UUID = 0x113B
    CTN_Access_Service = 0x113C
    CTN_Notification_Service = 0x113D
    CTN_Profile = 0x113E
    PnPInformation = 0x1200
    GenericNetworking = 0x1201
    GenericFileTransfer = 0x1202
    GenericAudio = 0x1203
    GenericTelephony = 0x1204
    UPNP_Service = 0x1205
    UPNP_IP_Service = 0x1206
    ESDP_UPNP_IP_PAN = 0x1300
    ESDP_UPNP_IP_LAP = 0x1301
    ESDP_UPNP_L2CAP = 0x1302
    VideoSource = 0x1303
    VideoSink = 0x1304
    VideoDistribution = 0x1305
    HDP = 0x1400
    HDP_Source = 0x1401
    HDP_Sink = 0x1402

class psm_t(IntEnum):
    SDP = 0x0001 #See Bluetooth Service Discovery Protocol (SDP), Bluetooth SIG
    RFCOMM = 0x0003 #See RFCOMM with TS 07.10, Bluetooth SIG
    TCS_BIN = 0x0005 #See Bluetooth Telephony Control Specification / TCS Binary, Bluetooth SIG
    TCS_BIN_CORDLESS = 0x0007 #See Bluetooth Telephony Control Specification / TCS Binary, Bluetooth SIG
    BNEP = 0x000F #See Bluetooth Network Encapsulation Protocol, Bluetooth SIG
    HID_Control = 0x0011 #See Human Interface Device, Bluetooth SIG
    HID_Interrupt = 0x0013 #See Human Interface Device, Bluetooth SIG
    UPnP = 0x0015 #See [ESDP] , Bluetooth SIG
    AVCTP = 0x0017 #See Audio/Video Control Transport Protocol, Bluetooth SIG
    AVDTP = 0x0019 #See Audio/Video Distribution Transport Protocol, Bluetooth SIG
    AVCTP_Browsing = 0x001B #See Audio/Video Remote Control Profile, Bluetooth SIG
    UDI_C_Plane = 0x001D #See the Unrestricted Digital Information Profile [UDI], Bluetooth SIG
    ATT = 0x001F #See Bluetooth Core Specification.​​
    _3DSP = 0x0021 #​​See 3D Synchronization Profile, Bluetooth SIG.
    LE_PSM_IPSP = 0x0023 #​See Internet Protocol Support Profile (IPSP), Bluetooth SIG
    OTS = 0x0025 #See Object Transfer Service (OTS), Bluetooth SIG 
    
class data_element_type(IntEnum):
    NULL = 0
    UINT = 1
    SINT = 2
    UUID = 3
    STRING = 4
    BOOL = 5
    DATA_ELEMENT_SEQ = 6
    DATA_ELEMENT_ALT = 7
    URL = 8
    
class data_element_size_t(IntEnum):
    ONE = 0
    TWO = 1
    FOUR = 2
    EIGHT = 3
    SIXTEEN = 4
    IN_NEXT_U8 = 5
    IN_NEXT_U16 = 6
    IN_NEXT_U32 = 7  
    
class data_element():
    itemsize = 0
    def __init__(self, data):
        if len(data) == 0:
            self.element_type = data_element_type.NULL
            self.element_size_desc = 0
            self.element_size = 0
            self.element_data = b''
            return
        try:
            self.element_type = data_element_type(data[0] >>3)
        except:
            self.element_type = data[0] >>3
        self.element_size_desc = data_element_size_t(data[0] & 0x07)
        if self.element_size_desc <= data_element_size_t.SIXTEEN:
            self.element_size = 1 <<self.element_size_desc
            offset = 1
        elif self.element_size_desc == data_element_size_t.IN_NEXT_U8:
            self.element_size = data[1]
            offset = 2
        elif self.element_size_desc == data_element_size_t.IN_NEXT_U16:
            self.element_size = int.from_bytes(data[1:3], 'big')
            offset = 3
        elif self.element_size_desc == data_element_size_t.IN_NEXT_U32:
            self.element_size = int.from_bytes(data[1:5], 'big')
            offset = 5
            
        if self.element_type == data_element_type.NULL:
            self.element_data = None
        elif self.element_type == data_element_type.UINT:
            self.element_data = int.from_bytes(data[offset:offset+self.element_size], 'big')
        elif self.element_type == data_element_type.SINT:
            self.element_data = int.from_bytes(data[offset:offset+self.element_size], 'big', signed=True)
        elif self.element_type == data_element_type.UUID:
            self.element_data = data[offset:offset+self.element_size]
        elif self.element_type == data_element_type.DATA_ELEMENT_SEQ:
            count = self.element_size
            self.element_data = []
            while count >0:
                ele = data_element(data[offset:])
                offset += len(ele)
                count -= len(ele)
                self.element_data.append(ele)
        else:
            self.element_data = data[offset:offset+self.element_size]
                
    def __len__(self):
        if self.element_size_desc <= data_element_size_t.SIXTEEN:
            offset = 1
        elif self.element_size_desc == data_element_size_t.IN_NEXT_U8:
            offset = 2
        elif self.element_size_desc == data_element_size_t.IN_NEXT_U16:
            offset = 3
        elif self.element_size_desc == data_element_size_t.IN_NEXT_U32:
            offset = 5
        return self.element_size + offset
        
    def __repr__(self):
        format_str = 'data element {}: size={}'.format(self.element_type, self.element_size)
        if True: #type(self.element_data) != list:
            format_str += ', data={}'.format(self.element_data)
            self.repr = format_str
            return format_str
        format_str += ', data:\r\n'
        for d in self.element_data:
            format_str += '\r\n    {}'.format(d)
        self.repr = format_str
        return self.repr
        
# (current parser, next parser if current pass, next parser if current fail)
class node:
    def __init__(self, name):
        self.name = name        
        self.parent = None
        self.sons = []
        self.elder_brothers = []
        
    def add_son(self, son_node):
        son_node.parent = self
        self.sons.append(son_node)

    def __repr__(self):
        try:
            rep = self.repr
        except:
            self.repr = 'nodename={}'.format(self.name)
            if self.parent != None:
                self.repr += ', parent={}'.format(self.parent.name)
            if len(self.sons) >0:
                self.repr += ', 1st son={}'.format(self.sons[0].name)
            if self.previous_brother != None:
                self.repr += ', brother={}, '.format(self.previous_brother.name)
            rep = self.repr

        return rep
    
class tree:
    def __init__(self):
        self.create_protocol_tree()

    def create_protocol_tree(self):
        self.root = node('btsnoop_packet')
        self.root.previous_brother = None
        self.nodes = [self.root]
        new_added_nodes = [self.root]        
        for p in new_added_nodes:     
            # sons of new added node p
            previous_brother = None
            p_class = globals()[p.name]
            for c in p_class.__subclasses__(): 
                son_node = node(c.__name__)
                son_node.previous_brother = previous_brother
                previous_brother = son_node
                p.add_son(son_node)
                new_added_nodes.append(son_node)                
                self.nodes.append(son_node)

        '''for p in self.nodes:
            print(p)'''

    def find_protocol(self, data):
        search_node = self.root
        match_protocol = None
        while(search_node != None):
            protocol = globals()[search_node.name]
            if(protocol().match(data, dbg_en=False)): # yes
                match_protocol = protocol
                if len(search_node.sons) == 0:
                    break
                search_node = search_node.sons[-1]
            else:
                search_node = search_node.previous_brother
        return match_protocol   

@dataclass
class basedataclass:
  def __len__(self):
    n = 0
    for x in dataclasses.fields(self): 
      t = getattr(x, 'type')
      default = getattr(x, 'default')
      if t in [bytearray, str, data_element]:
        if default != None:
          n += len(default)
      else:
        n += t().itemsize
    return n
  
  def unpack1(self, data, endian='little', dbg_en=False):
    if len(data) < len(self):
      if dbg_en:
        print('unpack fail: length {} < {}'.format(len(data), len(self)))
      return None
    
    offset = 0  
    for x in dataclasses.fields(self): 
      default = getattr(x, 'default')
      fieldname = getattr(x, 'name')
      t = getattr(x, 'type')

      if dbg_en:
        print(fieldname)
      
      if t in [uint8, uint16, uint32, int8, int16, int32, UINT8, UINT16, UINT32]:
        L = t().itemsize
        value = int.from_bytes(data[offset:offset+L], endian)
        offset += L
      elif t in [uint16_be, uint32_be, UINT16_BE, UINT32_BE]:
        L = t().itemsize
        value = int.from_bytes(data[offset:offset+L], 'big')
        offset += L
      elif t == bdaddr_t:
        L = t().itemsize
        value = data[offset:offset+L]
        offset += L
      elif t == str:
        L = 0
        for x in data[offset:]:
          if x == 0x00:
            break
          L +=1
        value = str(data[offset:offset+L], 'utf-8')
        offset += L
      elif t in [bytearray]:
        if default == None:
          L = 0
        else:
          L = len(default)
        value = data[offset:offset+L]
        offset += L
      elif t == data_element:
        value = data_element(data[offset:])
        offset += len(value)
      else:
        if dbg_en:
          print('unpack fail: unknown type {}'.format(t))
        continue
        
      if default == None:
        if t == data_element:
          setattr(self, fieldname, value)   
        else:
          setattr(self, fieldname, t(value)) # type convert   
        continue
        
      if default != value:
        if dbg_en:
          print('unpack fail: {} not match {:x} != {:x}'.format(fieldname, value, default))
        return None
        
      setattr(self, fieldname, t(value))  # type convert      
    return self
    
  def unpack(self, data, endian='little', dbg_en=False):
    ret = self.unpack1(data, endian, dbg_en)
    return ret
    '''try:
        ret = self.unpack1(data, endian, dbg_en)
        return ret
    except Exception as e:
        print(e)
        return None'''

  def match(self, data, dbg_en=False):
    if self.unpack(data, dbg_en=dbg_en) == None:
      return False
    else:
      return True

@dataclass
class btsnoop_file(basedataclass):
  btsnp_flag: bytearray = b'btsnoop\x00'
  btsnp_version: uint32 = 0x01
  btsnp_lnk_type: uint32 = 1002
  btsnp_records: bytearray = None
    
@dataclass 
class btsnoop_packet(basedataclass):
  btsnp_origin_len: uint32_be = None
  btsnp_included_len: uint32_be = None
  btsnp_pkt_flags: UINT32_BE = None
  btsnp_drops: uint32_be = None
  btsnp_timestamp_s: uint32_be = None
  btsnp_timestamp_us: uint32_be = None 
  # payload not listed
    
@dataclass
class hci_cmd(btsnoop_packet):
    hci_flag: uint8 = 0x01
    hci_opcode: UINT16 = None
    hci_length: uint8 = None

@dataclass
class hci_reset(hci_cmd):
    hci_flag: uint8 = 0x01
    hci_opcode: UINT16 = 0x0c03
    hci_length: uint8 = 0x00 

@dataclass
class hci_create_connection(hci_cmd):
    hci_flag: uint8 = 0x01
    hci_opcode: UINT16 = 0x0405
    hci_length: uint8 = 13
    peer_addr: bdaddr_t = None
    acl_packet_types: uint16 = None
    page_scan_repetition_mode: uint8=None
    page_scan_mode: uint8=None
    clock_offset: uint16=None
    allow_role_switch: uint8=None
    

@dataclass
class hci_event(btsnoop_packet):
    hci_flag: uint8 = 0x04
    hci_code: UINT8 = None
    hci_length: uint8 = None
    
@dataclass
class hci_cmd_status(hci_event):
    hci_code: UINT8 = 0x0f
    hci_length: uint8 = 0x04
    hci_status: uint8 = None
    hci_num_packet: uint8 = None
    hci_opcode: UINT16 = None       

@dataclass
class hci_cmd_complete(hci_event):
    hci_code: UINT8 = 0x0e
    hci_length: uint8 = None
    hci_num_packet: uint8 = None
    hci_opcode: UINT16 = None
    hci_status: uint8 = None

@dataclass
class hci_connection_complete(hci_event):
    hci_code: UINT8 = 0x03
    hci_status: uint8 = None
    connection_handle: UINT16 = None
    peer_addr: bdaddr_t = None
    link_type: uint8 = None
    encrypt_mode: uint8 = None

@dataclass
class hci_disconnection_complete(hci_event):
    hci_code: UINT8 = 0x05
    hci_status: uint8 = None
    connection_handle: UINT16 = None
    reason: uint8 = None
    
@dataclass
class hci_remote_name_request_complete(hci_event):
    hci_code: UINT8 = 0x07
    hci_status: uint8 = None
    peer_addr: bdaddr_t = None
    name: str = None
    
@dataclass
class hci_read_remote_version_complete(hci_event):
    hci_code: UINT8 = 0x0c
    hci_status: uint8 = None
    handle: uint16 = None
    lmp_version: uint8 = None
    lmp_manufacture: uint16 = None
    lmp_subversion: uint16 = None
  		
@dataclass
class l2c_packet(btsnoop_packet):
    hci_flag: uint8 = None
    handle_pb_bc: uint16 = None
    hci_length: uint16 = None  
    pdu_len: uint16 = None
    cid:     UINT16 = None 

    def match(self, data, dbg_en=True):
        ret = self.unpack(data, dbg_en=dbg_en)
        if ret == None:
            return False
        if ret.hci_flag in [2,3]:
            return True
        return False
    
@dataclass
class l2c_signal(l2c_packet):
  cid:	UINT16 = 0x0001
  cod:  UINT8 = None
  identify:  np.uint8 = None
  cmd_len: np.uint16 = None
    
@dataclass
class l2c_con_req(l2c_signal):
  cod:  UINT8 = 0x02
  psm:  uint16 = None
  scid: UINT16 = None

@dataclass
class l2c_con_res(l2c_signal):
  cod:  UINT8 = 0x03
  dcid: uint16 = None
  scid: UINT16 = None
  result: uint16 = None

  
@dataclass
class l2c_psm(l2c_packet):
    def match(self, data, dbg_en=False):
        if super().match(data, dbg_en=dbg_en) == False:
            return False
        ret = self.unpack(data)
        if ret == None:
            return False
        if ret.cid >=0x40:
            return True
        return False

@dataclass
class sdp_packet(l2c_psm):
    cid:	UINT16 = 0xFFFF # set after l2c_conn_req
    sdp_pdu_id: uint8 = None
    sdp_transaction_id: uint16_be = None
    sdp_param_len: uint16_be = None

@dataclass
class sdp_search_attr_req(sdp_packet):
    sdp_pdu_id: uint8 = 0x06
    list_of_search_services: bytearray = None
    max_amount_of_attr_data: uint16 = None
    list_of_attributes: bytearray = None
    bytes_for_continuation: uint8 = 0
        
@dataclass
class sdp_search_attr_res(sdp_packet):
    sdp_pdu_id: uint8 = 0x07
    bytes_for_attribute_list: uint16_be = None  
    attribute_list: data_element = None
    
class btsnoop:
    def __init__(self, filename):
        self.filename = filename
        fp = open(filename, 'rb')
        self.btsnoop = fp.read()
        if not self.check_hdr():
            print('{} is not a btsnoop file'.format(filename))
            return None
        self.records = []
        self.parsed = []
        self.hci_commands = []
        self.hci_events = []
        self.hci_datain = [] # controller -> host
        self.hci_dataout = []
        self.extract_records()
        self.parse_records()
                
    def find_ticket_n(self):
        path = self.filename.split('\\')
        ticket_n = ''
        for x in path:
            try:
                ticket_n = int(x)
            except:
                continue
            break
        if ticket_n !='':
            return {'ticket': x}
        else:
            return {}
    
    def check_hdr(self):
        tmp = btsnoop_file()
        if tmp.unpack(self.btsnoop[0:len(tmp)], 'big') !=None:
            return True
        return False
        
    def extract_records(self):
        offset = 16
        while offset <len(self.btsnoop):
            hdr = btsnoop_packet()
            
            if hdr.unpack(self.btsnoop[offset: offset+len(hdr)], 'big') == None:
                print('Invalid btsnoop packet {}'.format(hexlify(btsnoop[offset: offset+len(hdr)])))
                break
            
            data = self.btsnoop[offset: offset+len(hdr)+hdr.btsnp_included_len]
            offset += len(data)
            self.records.append(data)      
    
    def parse_records(self):  
        pending_l2c_con_reqs = []
        self.connections = [] # (start, end, hci_connection_complete)
        protocol_tree = tree()
        idx = 0
        for r in self.records:
            protocol = protocol_tree.find_protocol(r)  
            hdr = protocol().unpack(r, dbg_en=False)
            
            if type(hdr) == hci_connection_complete and \
               hdr.hci_status == 0:
                conn = {"start": idx, "conn_complete": hdr, "oui": find_manufacture(hdr.peer_addr)}
                self.connections.append(conn)               
            elif type(hdr) == hci_disconnection_complete:
                if len(self.connections) >0:
                    self.connections[-1].update({"end": idx, "disc_complete": hdr})  
            elif type(hdr) == l2c_con_req:
                pending_l2c_con_reqs.append(hdr)
            elif type(hdr) == l2c_con_res:
                for x in pending_l2c_con_reqs: # find matching conn_req
                    if x.scid == hdr.scid and x.identify == hdr.identify:
                        psm = x.psm
                        if psm == psm_t.SDP:
                            for y in dataclasses.fields(sdp_packet):
                                if getattr(y, 'name') == 'cid':
                                    setattr(y, 'default', x.scid)
            elif type(hdr) == hci_remote_name_request_complete:
                if len(self.connections) >0:
                    self.connections[-1].update({"name": hdr.name})  
            elif type(hdr) == hci_read_remote_version_complete:
                if len(self.connections) >0:
                    self.connections[-1].update({"lmp_version": hdr.lmp_version})
                    self.connections[-1].update({"lmp_manufacture": hdr.lmp_manufacture})
                    self.connections[-1].update({"lmp_subversion": hdr.lmp_subversion})
            elif type(hdr) == sdp_search_attr_res:
                self.sdp_profile_descriptor(hdr)
                    
                    
            self.parsed.append((hdr, r[len(hdr):]))
            idx += 1           
        
    def sdp_profile_descriptor(self, r):
        if (type(r) != sdp_search_attr_res) or (r.attribute_list ==None) or \
           (type(r.attribute_list.element_data) != list) or \
           len(r.attribute_list.element_data) ==0 or \
           type(r.attribute_list.element_data[0].element_data) != list or \
           r.btsnp_pkt_flags !=1: # 1: acl in; 0: acl out
            return
        i = 0
        attribute_list = r.attribute_list.element_data[0].element_data    
        for x in attribute_list:
            i += 1
            if (x.element_type == data_element_type.UINT) and \
               (x.element_data == attribute_id_t.PROFILE_DESC_LIST):
                break
        if i <len(attribute_list):
            try:
                profile_uuid = attribute_list[i].element_data[0].element_data[0].element_data
            except:
                profile_uuid = b'\x00\x00'
            try:
                profile_uuid = service_class_t(int.from_bytes(profile_uuid, 'big'))
            except:
                profile_uuid = (int.from_bytes(profile_uuid, 'big'))
                print(profile_uuid)
            try:    
                profile_version = attribute_list[i].element_data[0].element_data[1].element_data
            except:
                profile_version = 0
            try:
                profile_version = str(profile_version>>8) + '.' + str(profile_version&0xff)
            except:
                print(profile_version)

            if len(self.connections) >0:
                new_profile = (profile_uuid, profile_version)
                if "services" in self.connections[-1]:
                    if new_profile not in self.connections[-1]['services']:
                        self.connections[-1]['services'].append(new_profile)
                else:
                    self.connections[-1].update({"services":[new_profile]})  
                    
    def get_remote_info(self):
        remote_info_list = []
        for x in self.connections:
            try:
                peer_addr = str(x['conn_complete'].peer_addr)
            except:
                continue # give up if remote address not known
            try:
                name = x['name']
            except:
                name = 'unknown'
            try:
                oui = x['oui']
            except:
                oui = 'unknown'
            try:
                manufacture = str(lmp_manufacture(x['lmp_manufacture']))
                version = str(lmp_version(x['lmp_version']))
                subversion = x['lmp_subversion']
            except:
                manufacture = 'unknown' 
                version = 'unknown' 
                subversion = 'unknown' 

            try:
                profiles = x['services']
            except:
                profiles = []
            
            remote_info_list.append({"peer_addr": peer_addr, \
                                     "name": name, \
                                     "oui": oui, \
                                     "lmp_manufacture": manufacture, \
                                     "lmp_version": version, \
                                     "lmp_subversion": subversion, \
                                     "profiles": profiles, \
                                     })
        return remote_info_list
        
    def get_acl_connections(self, disconnect_reason=8):
        connections = []
        for x in self.connections:
            try:
                reason = x['disc_complete'].reason
            except:
                continue
            if x['conn_complete'].hci_status == 0 and \
               reason == disconnect_reason:
                connections.append(x)
        return connections
                    
def all_encodings():
    modnames = set(
        [modname for importer, modname, ispkg in pkgutil.walk_packages(
            path=[os.path.dirname(encodings.__file__)], prefix='')])
    aliases = set(encodings.aliases.aliases.values())
    return modnames.union(aliases)     
    
def open_all_decoding(filename, mod):  
    result = ''
    try:
        fp = open(filename, mod, encoding='UTF-8')	    
        result = fp.read()
        fp.close()
    except:
        encoders = all_encodings() # some files may use cp1256 as encoder
        for enc in encoders:
            try:
                fp = open(filename, mod, encoding=enc)	    
                result = fp.read()
                fp.close()
            except Exception as e:
                continue
            break          
    return result   

def find_manufacture(addr):
    ouifile = open_all_decoding(r'oui\oui.csv', 'r')
    try:
        addr = str(addr)
        oui = addr[0:9].replace(':', '')
    except:
        oui = ''
    pos = ouifile.find(oui)
    man = 'unknown'
    if pos >0:
        man = ouifile[pos + len(oui) + 1:]
        pos2 = man.find('\n')
        if pos2 >0:
            man = man[0:pos2]
    return man

def process_database(database):
    ret = []
    filter = []
    for x in database:
        if 'conn_complete' not in x:
            print(x)
            continue
        try:
            name = x['name']
        except:
            name = 'unknown'
        f = (x['conn_complete'].peer_addr, name)
        if f not in filter:
            ret.append(x)
            filter.append(f)
        else:
            try:
                for y in ret:
                    if (y['conn_complete'].peer_addr, y['name']) == f:
                        y.update(x)
                        break
            except:
                pass
    return ret  
        
def test_btsnoop():
    database = []
    cnt = 200000
    for x in os.walk(r'C:\zuolongjun\logs_extracted'):
        # x[0] a sub folder 
        # x[1] all folders in x[0], not popular 
        # x[2] all file names in x[0]
        for y in x[2]:
            if y == 'btsnoop_hci.log':
                filename = x[0] + '\\' + y
                print(filename)
                snoop = btsnoop(filename)
                for conn in snoop.connections:
                    database.append(conn)

                cnt -=1
                if cnt == 0:
                    break
        if cnt == 0:
            break
    database = process_database(database)
    save_device_info(database)

from openpyxl import Workbook, load_workbook
def save_device_info(database):
    filename = 'bt_devices.xlsx'
    wb = load_workbook(filename)
    sheet = wb.active
    # find the last row
    row_cursor = 2
    while sheet['A{}'.format(row_cursor)].value != None:
        row_cursor += 1

        if row_cursor >1000:
            break
    for x in database:            
        try:
            sheet['A{}'.format(row_cursor)] = str(x['conn_complete'].peer_addr)
        except:
            sheet['A{}'.format(row_cursor)] = 'unknown'
        try:
            sheet['B{}'.format(row_cursor)] = x['name']
        except:
            sheet['B{}'.format(row_cursor)] = 'unknown'
        try:
            sheet['C{}'.format(row_cursor)] = x['oui']
        except:
            sheet['C{}'.format(row_cursor)] = 'unknown'

        try:
            sheet['D{}'.format(row_cursor)] = str(lmp_manufacture(x['lmp_manufacture']))
            sheet['E{}'.format(row_cursor)] = str(lmp_version(x['lmp_version']))
            sheet['F{}'.format(row_cursor)] = x['lmp_subversion']
        except:
            sheet['D{}'.format(row_cursor)] = 'unknown' 
            sheet['E{}'.format(row_cursor)] = 'unknown' 
            sheet['F{}'.format(row_cursor)] = 'unknown' 

        try:
            profiles = x['services']
        except:
            profiles = []
        for s in profiles:
            if s[0] == service_class_t.Handsfree:
                sheet['G{}'.format(row_cursor)] = s[1]
            elif s[0] == service_class_t.AdvancedAudioDistribution:
                sheet['H{}'.format(row_cursor)] = s[1]
            elif s[0] == service_class_t.AV_RemoteControl:
                sheet['I{}'.format(row_cursor)] = s[1]
            elif s[0] == service_class_t.PnPInformation:
                sheet['J{}'.format(row_cursor)] = s[1]
            elif s[0] == service_class_t.Message_Access_Profile:
                sheet['K{}'.format(row_cursor)] = s[1]
            elif s[0] == service_class_t.SerialPort:
                sheet['L{}'.format(row_cursor)] = s[1]
            elif s[0] == service_class_t.IrMCSync:
                sheet['M{}'.format(row_cursor)] = s[1]
                    
        row_cursor += 1
    wb.save(filename)

if __name__ == "__main__":  
    print('test_btsnoop')
    test_btsnoop()

'''for x in btsnp.parsed:
    print(x[0])
    print(hexlify(x[1]))'''
