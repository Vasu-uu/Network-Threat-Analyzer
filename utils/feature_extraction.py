import pandas as pd

TRAINED_FEATURES = [
    'dur', 'proto', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'smean', 'dmean',
    'sload', 'dload', 'sttl', 'dttl', 'sinpkt', 'dinpkt', 'swin', 'dwin',
    'sloss', 'dloss'
]

FEATURE_ALIASES = {
    'dur': ['duration', 'flow duration', 'time', 'dur'],
    'proto': ['protocol', 'protocol_type', 'proto', 'Protocol', 'transport protocol', 'prot'],
    'spkts': ['total fwd packets', 'source packets', 'fwd packet count', 'fwd_pkts', 'spkts'],
    'dpkts': ['total bwd packets', 'destination packets', 'bwd packet count', 'bwd_pkts', 'dpkts'],
    'sbytes': ['total length of fwd packets', 'src_bytes', 'fwd bytes', 'source bytes', 'sbytes'],
    'dbytes': ['total length of bwd packets', 'dst_bytes', 'bwd bytes', 'destination bytes', 'dbytes'],
    'smean': ['fwd packet length mean', 'avg fwd segment size', 'fwd pkt len mean', 'smean'],
    'dmean': ['bwd packet length mean', 'avg bwd segment size', 'bwd pkt len mean', 'dmean'],
    'sload': ['flow bytes/s', 'src bits/sec', 'sload', 'fwd load', 'source load'],
    'dload': ['flow packets/s', 'dst bits/sec', 'dload', 'bwd load', 'destination load'],
    'sttl': ['src ttl', 'fwd header length', 'source ttl', 'sttl'],
    'dttl': ['dst ttl', 'bwd header length', 'destination ttl', 'dttl'],
    'sinpkt': ['fwd iat mean', 'source interpacket time', 'sinpkt', 'iat fwd'],
    'dinpkt': ['bwd iat mean', 'destination interpacket time', 'dinpkt', 'iat bwd'],
    'swin': ['init_win_bytes_forward', 'source window', 'swin'],
    'dwin': ['init_win_bytes_backward', 'destination window', 'dwin'],
    'sloss': ['fwd psh flags', 'source loss', 'sloss'],
    'dloss': ['bwd psh flags', 'destination loss', 'dloss']
}

PROTOCOL_NAME_TO_NUMBER = {
    'hopopt': 0, 'icmp': 1, 'igmp': 2, 'tcp': 6, 'udp': 17, 'ipv6': 41, 'gre': 47,
    'esp': 50, 'ah': 51, 'icmpv6': 58, 'ospf': 89, 'auth': 113, 'pim': 103,
    'sctp': 132, 'mpls-in-ip': 137, 'arp': 254,

   
    **{proto: 200 + i for i, proto in enumerate([
        'rtp', 'ddp', 'ipv6-frag', 'cftp', 'wsn', 'pvp', 'wb-expak', 'mtp', 'pri-enc',
        'sat-mon', 'cphb', 'sun-nd', 'iso-ip', 'xtp', 'il', 'unas', 'mfe-nsp', '3pc',
        'ipv6-route', 'idrp', 'bna', 'swipe', 'kryptolan', 'cpnx', 'rsvp', 'wb-mon',
        'vmtp', 'ib', 'dgp', 'eigrp', 'ax.25', 'gmtp', 'pnni', 'sep', 'pgm', 'idpr-cmtp',
        'zero', 'rvd', 'mobile', 'narp', 'fc', 'pipe', 'ipcomp', 'ipv6-no', 'sat-expak',
        'ipv6-opts', 'snp', 'ipcv', 'br-sat-mon', 'ttp', 'tcf', 'nsfnet-igp', 'sprite-rpc',
        'aes-sp3-d', 'sccopmce', 'qnx', 'scps', 'etherip', 'aris', 'compaq-peer', 'vrrp',
        'iatp', 'stp', 'l2tp', 'srp', 'sm', 'isis', 'smp', 'fire', 'ptp', 'crtp', 'sps',
        'merit-inp', 'idpr', 'skip', 'any', 'larp', 'ipip', 'micp', 'encap', 'ifmp',
        'tp++', 'a/n', 'i-nlsp', 'ipx-n-ip', 'sdrp', 'tlsp', 'mhrp', 'ddx', 'ippc', 'visa',
        'secure-vmtp', 'uti', 'vines', 'crudp', 'iplt', 'ggp', 'ip', 'ipnip', 'st2',
        'argus', 'bbn-rcc', 'egp', 'emcon', 'igp', 'nvp', 'pup', 'xnet', 'chaos', 'mux',
        'dcn', 'hmp', 'prm', 'trunk-1', 'xns-idp', 'leaf-1', 'leaf-2', 'rdp', 'irtp',
        'iso-tp4', 'netblt', 'trunk-2', 'cbt'
    ])}
}

PROTOCOL_NUMBER_TO_NAME = {v: k.upper() for k, v in PROTOCOL_NAME_TO_NUMBER.items()}

CATEGORICAL_FEATURES = ['proto']

def normalize(name):
    return name.strip().lower().replace(' ', '').replace('_', '')

def resolve_alias(possible_aliases, norm_cols):
    for alias in possible_aliases:
        norm_alias = normalize(alias)
        if norm_alias in norm_cols:
            return norm_cols[norm_alias]
    return None

def extract_features_from_df(df):
    df.columns = df.columns.str.strip()
    norm_cols = {normalize(col): col for col in df.columns}
    col_map = {}

    for std_feature in TRAINED_FEATURES:
        aliases = FEATURE_ALIASES.get(std_feature, [std_feature])
        resolved = resolve_alias(aliases, norm_cols)
        if resolved:
            col_map[std_feature] = resolved

    if not col_map:
        raise ValueError("No matching features found in input")

    for cat_feat in CATEGORICAL_FEATURES:
        if cat_feat in col_map:
            original_col = col_map[cat_feat]
            proto_col_data = df[original_col].astype(str).str.strip().str.lower()
            df[original_col] = proto_col_data.apply(lambda val: PROTOCOL_NAME_TO_NUMBER.get(val, -1))

            unknowns = proto_col_data[proto_col_data.apply(lambda x: x not in PROTOCOL_NAME_TO_NUMBER)].unique()
            if len(unknowns) > 0:
                print("[WARN] Unknown protocol types found:", list(unknowns))

    selected = df[[col_map[f] for f in col_map]].copy()
    selected.columns = list(col_map.keys())

    selected = selected.replace([float('inf'), -float('inf')], pd.NA)
    selected = selected.apply(pd.to_numeric, errors='coerce')
    valid_idx = selected.dropna().index

    proto_col = col_map.get('proto')
    proto_vals = df[proto_col] if proto_col and proto_col in df.columns else pd.Series(['N/A'] * len(df))

    def decode_proto(val):
        try:
            val_int = int(val)
            return PROTOCOL_NUMBER_TO_NAME.get(val_int, f'Unknown({val_int})')
        except:
            return str(val)

    original_info = pd.DataFrame(index=selected.index)
    original_info['Protocol'] = proto_vals.loc[valid_idx].apply(decode_proto)
    original_info['Source IP'] = df.get('Source IP', pd.Series(['N/A'] * len(df))).loc[valid_idx]
    original_info['Destination IP'] = df.get('Destination IP', pd.Series(['N/A'] * len(df))).loc[valid_idx]

    return selected.loc[valid_idx].reset_index(drop=True), original_info.reset_index(drop=True)
