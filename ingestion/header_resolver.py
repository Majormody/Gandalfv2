
def resolve_headers(data: list[list]) -> tuple[list[str], list[list]]:
    
        if len(data) < 2 :
            return (data[0] if data else []),[]

        none_vals = 0
        merged = 0
        headers = []   
        for val in data[0]:
            if val == None:
                none_vals +=1
        if none_vals >= len(data[0])/2:
            merged = 1

        for a, b in zip(data[0], data[1]):
            if a is None and b is None:
                merged = 0
                break
        if not merged:
            for i in range(len(data[0])):
                headers.append((data[0][i] if data[0][i] else ''))
            vals = data[1:]
            return headers, vals

      # if merged:   
        for a,b in zip(data[0], data[1]):
            headers.append((a if a else '') + ' ' +(b if b else '') )
        vals = data[2:]
        return headers, vals
                
            