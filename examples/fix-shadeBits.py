import re

with open('example-gallery.tex', 'r') as f:
    content = f.read()

# Remove the incorrect additions
content = re.sub(r'  \\shadeBetweenBits\{000111\}\{110001\}\{LB1\}\{UB1\}\n', '', content)

# Now add them correctly based on context
lines = content.split('\n')
result = []
i = 0
while i < len(lines):
    line = lines[i]
    result.append(line)
    
    # If this is a \shadeBetween call, look backwards for the path declarations
    if '\\shadeBetween[fill=' in line:
        # Extract the path names from \shadeBetween
        match = re.search(r'\\shadeBetween\[.*?\]\{(\w+)\}\{(\w+)\}', line)
        if match:
            lname, uname = match.groups()
            
            # Look backwards for the path declarations
            l_bits = None
            u_bits = None
            for j in range(i-1, max(0, i-20), -1):
                if f'\\lpDeclarePath{{{lname}}}' in lines[j]:
                    lmatch = re.search(r'\\lpDeclarePath\{' + lname + r'\}\{([01]+)\}', lines[j])
                    if lmatch:
                        l_bits = lmatch.group(1)
                if f'\\lpDeclarePath{{{uname}}}' in lines[j]:
                    umatch = re.search(r'\\lpDeclarePath\{' + uname + r'\}\{([01]+)\}', lines[j])
                    if umatch:
                        u_bits = umatch.group(1)
                        
            if l_bits and u_bits:
                # Check if \shadeBetweenBits is already on the previous line
                if i > 0 and '\\shadeBetweenBits' not in lines[i-1]:
                    # Get the indentation of the current line
                    indent = len(line) - len(line.lstrip())
                    # Insert the \shadeBetweenBits call before this line
                    result.insert(-1, ' ' * indent + f'\\shadeBetweenBits{{{l_bits}}}{{{u_bits}}}{{{lname}}}{{{uname}}}')
    
    i += 1

with open('example-gallery.tex', 'w') as f:
    f.write('\n'.join(result))

print("Fixed shadeBetween calls")
