import requests
import json

traversed = []

def getstate(fullurl):
    get_state = requests.get(url=fullurl)
    counter = 0
    list = []

    size = ""
    cl = ""
    status = ""
    lvls = ""
    totlvls = ""

    for c in get_state.text:
        if c == '}':
            continue
        if c == '\"':
            counter += 1
            continue
        if counter == 2:
            if (c == ':' or c == '[' or c == ']'):
                continue
            else:
                size += c
        if counter == 4:
            if (c == ':' or c == '[' or c == ']'):
                continue
            else:
                cl += c
        if counter == 7:
            status += c
        if counter == 10:
            if (c == ':' or c == ','):
                continue
            else:
                lvls += c
        if counter == 12:
            if (c == ':' or c == ','):
                continue
            else:
                totlvls += c

    comma = False
    x = ""
    y = ""

    for c in size:
        if c == ',':
            comma = True
            continue
        if not comma:
            x += c
        if comma:
            y += c

    if x.isdigit():
        list.append(int(x))
    else:
        list.append(0)

    if y.isdigit():
       list.append(int(y))
    else:
       list.append(0)

    comma = False
    x = ""
    y = ""

    for c in cl:
        if c == ",":
            comma = True
            continue
        if not comma:
            x += c
        if comma:
            y += c

    if x.isdigit():
        list.append(int(x))
    else:
        list.append(None)

    if y.isdigit():
        list.append(int(y))
    else:
        list.append(None)

    list.append(status)

    if lvls.isdigit():
        list.append(int(lvls))
    else:
        list.append(None)

    if totlvls.isdigit():
        list.append(int(totlvls))
    else:
        list.append(None)

    return list

def getkey():
    get_token = requests.post(url="http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session",
                              data={"uid":"304805526"})
    counter = 0
    key = ""
    for c in get_token.text:
        if c == '\"':
            counter += 1
            continue
        if counter == 3:
            key += c
    return key

def traverse(fullurl, dir, cl, ol, path):
    result = ""
    x = cl[0]
    y = cl[1]

    # upl = (x, y - 1)
    # downl = (x, y + 1)
    # leftl = (x - 1, y)
    # rightl = (x + 1, y)

    # upv = False
    # downv = False
    # leftv = False
    # rightv = False

    up = False
    down = False
    left = False
    right = False

    # print("-----")
    # print(dir)
    # print(traversed)

    visited = False

    if dir == "UP":
        y -= 1

    if dir == "DOWN":
        y += 1

    if dir == "LEFT":
        x -= 1

    if dir == "RIGHT":
        x += 1

    nl = (x, y)

    # print(traversed)
    for loc in traversed:
        # if loc == upl:
        #     print("up true")
        #     print(loc)
        #     print(upl)
        #     print("why")
        #     upv = True
        # if loc == downl:
        #     downv = True
        # if loc == leftl:
        #     leftv = True
        # if loc == rightl:
        #     rightv = True
        if loc == nl:
            # print("traversed")
            visited = True


    # print("nl")
    # print(nl)
    # print("cl")
    # print(cl)
    # print("ol")
    # print(ol)

    if not visited:
        # print("append")
        # print(nl)
        traversed.append(nl)

    # else:
    #     if (cl[0] - ol[0]) == 1: # came from left
    #         print("first go back left")
    #         requests.post(url = fullurl, data = {"action":"LEFT"})
    #     if (cl[0] - ol[0]) == -1: # came from right
    #         print("first go back right")
    #         requests.post(url = fullurl, data = {"action":"RIGHT"})
    #     if (cl[1] - ol[1]) == 1: # came from top
    #         print("first go back up")
    #         requests.post(url = fullurl, data = {"action":"UP"})
    #     if (cl[0] - ol[0]) == 1: # came from bottom
    #         print("first go back down")
    #         requests.post(url = fullurl, data = {"action":"DOWN"})

        post = requests.post(url = fullurl, data = {"action":dir})

        counter = 0

        for c in post.text:
            if c == '\"':
                counter += 1
                continue
            if counter == 3:
                result += c

        # print(result)

        if result == "END":
            return True

        upv = False
        downv = False
        leftv = False
        rightv = False

        upl = (nl[0], nl[1] - 1)
        downl = (nl[0], nl[1] + 1)
        leftl = (nl[0] - 1, nl[1])
        rightl = (nl[0] + 1, nl[1])

        for loc in traversed:
            if loc == upl:
                upv = True
            if loc == downl:
                downv = True
            if loc == leftl:
                leftv = True
            if loc == rightl:
                rightv = True

        # state = getstate(fullurl)
        # print(state)

        # print(upv)
        # print(downv)
        # print(leftv)
        # print(rightv)

        if result == "SUCCESS":
            path.append(nl)
            if not upv:
                # print("traverse up")
                up = traverse(fullurl, "UP", nl, cl, path)
                if up:
                    return up
                # if up == False:
                #     requests.post(url = fullurl, data = {"action":"DOWN"})

            if not downv:
                # print("traverse down")
                down = traverse(fullurl, "DOWN", nl, cl, path)
                if down:
                    return down
                # if down == False:
                #     requests.post(url = fullurl, data = {"action":"UP"})

            if not leftv:
                # print("traverse left")
                left = traverse(fullurl, "LEFT", nl, cl, path)
                if left:
                    return left
                # if left == False:
                #     requests.post(url = fullurl, data = {"action":"RIGHT"})

            if not rightv:
                # print("traverse right")
                right = traverse(fullurl, "RIGHT", nl, cl, path)
                if right:
                    return right
                # if right == False:
                #     requests.post(url = fullurl, data = {"action":"LEFT"})

            # print(up)
            # print(down)
            # print(left)
            # print(right)

            if not (up or down or left or right):
                # print("trying to return, I'm sad")
                # print(cl)
                cl = path.pop()
                pl = path.pop()
                path.append(pl)

                # print(nl)
                # print(pl)
                if (nl[0] - pl[0]) == 1: # came from left
                    # print("go back left")
                    requests.post(url = fullurl, data = {"action":"LEFT"})
                if (nl[0] - pl[0]) == -1: # came from right
                    # print("go back right")
                    requests.post(url = fullurl, data = {"action":"RIGHT"})
                if (nl[1] - pl[1]) == 1: # came from top
                    # print("go back up")
                    requests.post(url = fullurl, data = {"action":"UP"})
                if (nl[1] - pl[1]) == -1: # came from bottom
                    # print("go back down")
                    requests.post(url = fullurl, data = {"action":"DOWN"})

    # pl = path.pop()
    # print(pl)
    # if not (up or down or left or right):
    #     print(cl)
    #     print(pl)
    #     if (cl[0] - pl[0]) == 1: # came from left
    #         print("go back left")
    #         requests.post(url = fullurl, data = {"action":"LEFT"})
    #     if (cl[0] - pl[0]) == -1: # came from right
    #         print("go back right")
    #         requests.post(url = fullurl, data = {"action":"RIGHT"})
    #     if (cl[1] - pl[1]) == 1: # came from top
    #         print("go back up")
    #         requests.post(url = fullurl, data = {"action":"UP"})
    #     if (cl[1] - pl[1]) == -1: # came from bottom
    #         print("go back down")
    #         requests.post(url = fullurl, data = {"action":"DOWN"})

    # print("returning")
    return up or down or left or right

def main():
    # print("start")
    key = getkey()
    # print("got key")
    fullurl = "http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=" + key
    state = getstate(fullurl)

    while(state[4] == "PLAYING"):
        # print("loading game map")
        traversed.clear()
        state = getstate(fullurl)
        print(state)
        x = state[2]
        y = state[3]

        if(state[4] != "PLAYING"):
            break
        # xb = state[0] - 1
        # yb = state[1] - 1
        cl = (x, y)
        traversed.append(cl)

        for dir in ["UP", "DOWN", "LEFT", "RIGHT"]:
            # print("/////////////////////")
            path = [cl]
            res = traverse(fullurl, dir, cl, cl, path)
            # print("am I done?!?!?!??!?!?!?!?!?!?!?!?!??!?!")
            if res == True:
                break

    #getstate(fullurl)

if __name__ == '__main__':
    main()
