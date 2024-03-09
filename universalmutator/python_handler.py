import marshal
import os
import sys
import py_compile
import uuid


def buildCode(c):
    val = []
    try:
        val.append(c.co_code)
    except BaseException:
        if type(c) == str:
            val.append("@STRING@:" + c)
        else:
            val.append(c)
    try:
        for cc in c.co_consts:
            bc = buildCode(cc)
            try:
                if bc[0].find("@STRING@") == 0:
                    bc = bc[1:]
            except BaseException:
                pass
            val.append(bc)
    except BaseException:
        pass
    return tuple(val)


def getPythonCode(fname):
    # from https://stackoverflow.com/questions/32562163/how-can-i-understand-a-pyc-file-content
    header_sizes = [
        # (size, first version this applies to)
        # pyc files were introduced in 0.9.2 way, way back in June 1991.
        (8,  (0, 9, 2)),  # 2 bytes magic number, \r\n, 4 bytes UNIX timestamp
        (12, (3, 6)),     # added 4 bytes file size
        # bytes 4-8 are flags, meaning of 9-16 depends on what flags are set
        # bit 0 not set: 9-12 timestamp, 13-16 file size
        # bit 0 set: 9-16 file hash (SipHash-2-4, k0 = 4 bytes of the file, k1 = 0)
        (16, (3, 7)),     # inserted 4 bytes bit flag field at 4-8 
        # future version may add more bytes still, at which point we can extend
        # this table. It is correct for Python versions up to 3.9
    ]
    header_size = next(s for s, v in reversed(header_sizes) if sys.version_info >= v)

    with open(fname, "rb") as f:
        metadata = f.read(header_size)  # first header_size bytes are metadata
        try:
            code = marshal.load(f)          # rest is a marshalled code object
        except:
            print("WARNING: UNABLE TO MARSHAL CODE FROM PYC FILE!")
            return(uuid.uuid4())
    if ("code" not in str(type(code))):
        print("WARNING: INVALID CODE OBJECT READ FROM PYC FILE!")
        return(uuid.uuid4())        
    b = buildCode(code)
    return b


def handler(tmpMutantName, mutant, sourceFile, uniqueMutants):
    compiled = tmpMutantName.replace(".py", ".pyc")

    if os.path.exists(compiled):
        os.remove(compiled)

    try:
        py_compile.compile(tmpMutantName, doraise=True, cfile=compiled)
    except py_compile.PyCompileError:
        return "INVALID"

    if len(uniqueMutants) == 0:
        sourceCompiled = sourceFile.replace(".py", ".pyc")
        py_compile.compile(sourceFile, cfile=sourceCompiled)
        if os.path.exists(sourceCompiled):
            uniqueMutants[getPythonCode(sourceCompiled)] = 1

    if os.path.exists(compiled):
        code = getPythonCode(compiled)
        if code in uniqueMutants:
            uniqueMutants[code] += 1
            return "REDUNDANT"
        else:
            uniqueMutants[code] = 1
            return "VALID"
    else:
        return "INVALID"
