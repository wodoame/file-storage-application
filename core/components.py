from .models import Folder, File
from .utils import getSVG
from django.db.models import QuerySet
import asyncio 

# * Shows the file and folder icons 
def renderFiles(request, username, id):
    result = ''
    folder = Folder.objects.get(id=id) 
    files: QuerySet = folder.files.all() 
    subFolders: QuerySet = folder.sub_folders.all()
    everything = list(files) + list(subFolders)
    everything.sort(key=lambda x: x.created)
    # asyncio.run(asyncio.sleep(5)) # intentional delay
    for item in everything: 
        url = f"/{username}/{item.id}/" if item.isFolder() else f'/download/{item.id}/'
        result += f"""
            <li class="mb-3 rounded file" x-data="{{'open':false}}">
                <div class="dots rounded" @click="open=!open">
                    <svg role="button" class="dropdown-toggle" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" style="fill: steelblue;"><path d="M12 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 0c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM6 10c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg>               
                </div>
                    <div x-show="open" class="dropdown-content rounded" @click.outside="open=false">
                        <ul>
                            <li class="hoverable">
                             <a href="{url if not item.isFolder() else '#'}"><span><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" class="dark:fill-gray-400 fill-gray-800"><path d="M18.948 11.112C18.511 7.67 15.563 5 12.004 5c-2.756 0-5.15 1.611-6.243 4.15-2.148.642-3.757 2.67-3.757 4.85 0 2.757 2.243 5 5 5h1v-2h-1c-1.654 0-3-1.346-3-3 0-1.404 1.199-2.757 2.673-3.016l.581-.102.192-.558C8.153 8.273 9.898 7 12.004 7c2.757 0 5 2.243 5 5v1h1c1.103 0 2 .897 2 2s-.897 2-2 2h-2v2h2c2.206 0 4-1.794 4-4a4.008 4.008 0 0 0-3.056-3.888z"></path><path d="M13.004 14v-4h-2v4h-3l4 5 4-5z"></path></svg></span><span>Download</span></a>
                            </li>
                            <li class="hoverable">
                                <a><span><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" class="dark:fill-gray-400 fill-gray-800"><path d="M3 12c0 1.654 1.346 3 3 3 .794 0 1.512-.315 2.049-.82l5.991 3.424c-.018.13-.04.26-.04.396 0 1.654 1.346 3 3 3s3-1.346 3-3-1.346-3-3-3c-.794 0-1.512.315-2.049.82L8.96 12.397c.018-.131.04-.261.04-.397s-.022-.266-.04-.397l5.991-3.423c.537.505 1.255.82 2.049.82 1.654 0 3-1.346 3-3s-1.346-3-3-3-3 1.346-3 3c0 .136.022.266.04.397L8.049 9.82A2.982 2.982 0 0 0 6 9c-1.654 0-3 1.346-3 3z"></path></svg></span> <span>Share</span></a>
                            </li>
                            <li class="hoverable">
                                <a><span><svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" class="dark:fill-gray-400 fill-gray-800"><path d="M5 20a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8h2V6h-4V4a2 2 0 0 0-2-2H9a2 2 0 0 0-2 2v2H3v2h2zM9 4h6v2H9zM8 8h9v12H7V8z"></path><path d="M9 10h2v8H9zm4 0h2v8h-2z"></path></svg></span> <span>Delete</span></a>
                            </li>
                        </ul>
                    </div>
                
                <div class="flex justify-center">
                    {getSVG('folder') if item.isFolder() else getSVG(item.extension)}
                </div>

                
                <a href="{url if item.isFolder() else '#'}" class="filename block dark:text-gray-400 text-gray-600 text-center mt-1 truncate">
                    {item.name}
                </a>
            </li>
        """
    return result

from collections import deque
# * Shows the file path
def renderPath(pathString: str, ids: deque, username: str) -> str:
    result = ''
    dirNames = pathString.split('/')
    # ? Is it possible to use utils.getExtension() to determine if the dirName is a file or forlder name ? I think so.
    # * For now it's only going to be folders
    for i, dirName in enumerate(dirNames): 
        result += f"""
              <li>
                <div class="flex items-center gap-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    class="h-4 w-4 stroke-current">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"></path>
                  </svg>
                  <a href="/{username}/{ids[i]}/">
                    {dirName}
                  </a>
                </div>
              </li>
          </div>
        """
    return result

import re
from django.contrib.auth.models import User
def generateSearch(q, id):
    # fuzzysearch library by python might be interesting to explore
    # some article to learn more about fuzzy search: https://typesense.org/learn/fuzzy-string-matching-python/
    # * At the moment this search works for searching for users
    result = ''
    pattern = re.compile(q, re.IGNORECASE)
    files = Folder.objects.get(id=id).files.all()
    limit = 5
    count = 0
    # asyncio.run(asyncio.sleep(5))
    for user in User.objects.all():
        if count == limit: 
            break
        displayText = f'{user.username} {user.email}'
        match = re.search(pattern, displayText)
        if match:
             count += 1 # increment the number of matches found
             span = match.span() # (start index, end index + 1)
             displayText = displayText[:span[0]] + '<span class="font-bold text-sky-500">' + displayText[span[0]: span[1]] + '</span>' + displayText[span[1]:]
            #  print(displayText)
             result += f"""
                    <li class="hoverable px-2 py-1 rounded-md cursor-pointer">
                        <a href="/{user.username}/">
                            {displayText}
                        </a>
                    </li>
             """
    count = 0     
    for file in files: 
        if count == limit: 
            break
        displayText = f'{file.name}'
        match = re.search(pattern, displayText)
        if match:
             count += 1 # increment number the matches found
             span = match.span() # (start index, end index + 1)
             displayText = displayText[:span[0]] + '<span class="font-bold text-sky-500">' + displayText[span[0]: span[1]] + '</span>' + displayText[span[1]:]
             print(displayText)
             result += f"""
                    <li class="hoverable px-2 py-1 rounded-md cursor-pointer">
                        <a href="#" class="flex gap-2">
                            <div class="flex justify-center items-center">{getSVG(file.extension, 20)}</div>
                            <div>
                             {displayText}
                            </div>
                        </a>
                    </li>
             """
    return result
    