import argparse, requests, re
from datetime import datetime
markdownify = None # Optional import , safely lazy-loaded

headers = {
    'authority': 'tryhackme.com',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://tryhackme.com/dashboard',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
s = requests.Session()
s.headers.update(headers)

def fetch(args, hasEnteredSid=False):
    # resp = s.get('https://tryhackme.com/room/{}'.format(args.room)) # Normal room page itself
    resp = s.get('https://tryhackme.com/api/room/details?codes={}&loadWriteUps=false&loadCreators=true&loadUser=false'.format(args.room), allow_redirects=False) # Use API instead
    details = None
    try:
        details = resp.json()
    except:
        pass
    if details and details[args.room] and details[args.room]['success']:

        # Got details, start building markdown with room metadata
        details = details[args.room]
        doc = ""
        if details['headerImage']:
            doc += "![{}]({})\n\n".format(details['title'], details['headerImage'])
        elif details['image']:
            doc += "![{}]({} =200x150)\n\n".format(details['title'], details['image'])
        doc += "# {}\n\n".format(details['title'])
        doc += "***{}***\n\n".format(details['description'])
        doc += "`{}`\n\n".format('`, `'.join(['#'+t for t in details['tags']]))
        doc += "[Link to room](https://tryhackme.com/room/{})\n\n".format(args.room)
        doc += "**Author{}:** *{}*\n\n".format(
            's' if len(details['creators']) > 1 else '',
            ','.join(['[{u}](https://tryhackme.com/p/{u})'.format(u=c['username']) for c in details['creators']])
        )
        doc += "Room published: {}\n\n".format(datetime.strptime(details['published'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%Y-%m-%d %H:%M"))
        doc += "Room started: {}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"))
        doc += "Room finished: \n\n"

        # Now try fetch questions
        resp = s.get('https://tryhackme.com/api/tasks/{}'.format(args.room), allow_redirects=False)
        tasks = None
        try:
            tasks = resp.json()
        except:
            pass
        if tasks and tasks['success']:

            # Try import markdownify
            global markdownify
            if not markdownify:
                try:
                    from markdownify import markdownify
                except:
                    pass
            if not markdownify:
                args.disable_markdown = True

            # Got questions, append to markdown doc
            for i, task in enumerate(tasks['data']):
                doc += "## Task {}: {}\n\n".format(i+1,task['taskTitle'])
                if args.verbose:
                    doc += re.sub('>','&gt;',re.sub('<','&lt;',markdownify(task['taskDesc'])))+"\n\n" if not args.disable_markdown else task['taskDesc']+"\n\n"
                for q in task['questions']:
                    doc += "{}) {}\n\n".format(
                        q['questionNo'],
                        re.sub('>','&gt;',re.sub('<','&lt;',markdownify(q['question']))) if not args.disable_markdown else q['question']
                    )
                    doc += "```\n\n```\n\n"
            
            # Tidy up any extra new lines
            doc = re.sub(' *\n[\n ]+','\n\n',doc)

            # Output to file, or console
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(doc)
                print('Output written to ./{}'.format(args.output.replace('\\','/')))
            else:
                print(doc)
            
        else:
            # Something went wrong, is it for subscription members only?
            if resp.status_code >= 300:
                if 'Location' in resp.headers and 'subscribe' in resp.headers['Location']:
                    if not hasEnteredSid:
                        print('Looks like this is a subscriber only room.')
                        sid = input('Enter value of your \'connect.sid\' cookie: ')
                        s.cookies.update({'connect.sid': sid.strip()})
                        return fetch(args, True)
                    else:
                        print('Error: Could not load tasks for premium room \'{}\''.format(args.room))
                else:
                    print('Error loading tasks for room code \'{}\': {} returned'.format(args.room, resp.status_code))
            elif tasks:
                print('Error loading tasks for room code \'{}\': success {}'.format(args.room, tasks['success']))
            else:
                print('Error: could not load tasks for room code \'{}\''.format(args.room))
        
    else:
        print('Error: unknown room code {}'.format(args.room))

def main():
    parser = argparse.ArgumentParser(description='TryHackMe Room Markdown Note Generator')
    parser.add_argument('room',                                          help="Room code (from the room URL)")
    parser.add_argument('-o', '--output',                                help="Output to file")
    parser.add_argument('-d', '--disable-markdown', action='store_true', help="Disable changing question HTML to markdown format")
    parser.add_argument('-v', '--verbose',          action='store_true', help="Verbose output (includes task descriptions)")
    args = parser.parse_args()
    
    fetch(args)

# Begin script
if __name__ == "__main__": main()