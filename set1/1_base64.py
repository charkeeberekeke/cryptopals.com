#http://cryptopals.com/sets/1/challenges/1/

def hex_iterator(s, n):
    """
    Iterator to generate list of integers taken from n hex characters
    from a string s
    """
    for i in range(0, len(s), n):
        try:
            yield int(s[i:i+n], 16)
        except IndexError:
            yield int(s[i:], 16)
            
def bit_lead_mask(n, b, l):
    """
    Takes number n, leading bits of length b out of number with bit length l
    Returns a tuple with, the first as the leading b digits from number n, and
    the second as the remainder
    example:
    n = 0b10101000, b = 6, l = 8
    bit_lead_mask(n, b, l) = (0b101010, 00)
    """
    mask = ((1 << b) - 1) << (l-b) # all ones at length b + all 0s at length (l-b)
    return (n & mask) >> (l-b), (n & (1 << (l-b)) - 1)

def b64_unit(nums):
    """
    Takes list of integers up to length 3, and returns
    base64 equivalent
    """
    ret = []
    tmp = 0
    l = len(nums)
    
    for n in range(l):
        tmp += nums[n] << (8*(l-n-1))
    #print "{0:b}".format(tmp)
        
    bits = l * 8
    padded = False
    
    while bits > 0:
        """
        The writtedn code doesn't look nice, 
        but I'd rather write in uniform code than do
        a length dependent, akin to a c switch, code
        """
        if padded:
            if bits < 6:
                tmp = tmp << 8
                bits += 8
            ret.append(64)
            bits-=6
            continue
            
        if bits < 6:
            tmp = tmp << 8
            bits += 8
            padded = True

        b, tmp = bit_lead_mask(tmp, 6, bits)
        ret.append(b)
        bits-=6
        
    return ret     

def b64_to_char(b):
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    return s[b]

def b64_decode(s):
    """
    Tying it all together
    """
    hexs = list(hex_iterator(s,2))
    return "".join( [b64_to_char(b) for h in range(0, len(hexs), 3) for b in b64_unit(hexs[h:h+3])] )

def string_to_ascii(s, format_spec):
    """
    Convert string to ascii according to format_spec
    Example is convert `Hello World` to format similar to given string in this exercise,
    for consumption of b64_decode() function
    string_to_ascii("Hello World", 'x') = '48656c6c6f20576f726c64'
    """
    return "".join([ format(ord(_s), format_spec) for _s in s])

"""
To test:            
s = "9276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
print b64_decode(convert_to_ascii)
"""
