import numpy as np

def obj_count(array, dim, shape):
    array = array.reshape(shape)
    if dim == 'x':
        nobjx = np.int64(array[0, :, :])
        for i in range(shape[0] - 1):
            mask1 = ~array[i, :, :] & array[i + 1, :, :]
            nobjx[mask1] += 1
        return nobjx
    elif dim == 'y':
        nobjy = np.int64(array[:, 0, :])
        for j in range(shape[1] - 1):
            mask2 = ~array[:, j, :] & array[:, j + 1, :]
            nobjy[mask2] += 1
        return nobjy
    else:
        nobjz = np.int64(array[:, :, 0])
        for k in range(shape[2] - 1):
            mask3 = ~array[:, :, k] & array[:, :, k + 1]
            nobjz[mask3] += 1
        return nobjz

def get_boundaries(array, dim, shape, lx, ly, lz, nobjmax, dd):
    array = array.reshape(shape)
    if dim == 'x':
        xi = np.zeros((nobjmax, shape[1], shape[2]))
        xf = np.zeros((nobjmax, shape[1], shape[2]))

        for k in range(shape[2]):
            for j in range(shape[1]):
                inum = 0
                if array[1, j, k]:
                    xi[inum, j, k] = -dd[0]

                for i in range(shape[0] - 1):
                    if not array[i, j, k] and array[i + 1, j, k]:
                        xi[inum, j, k] = dd[1] * i + dd[1] / 2
                    elif array[i, j, k] and not array[i + 1, j, k]:
                        xf[inum, j, k] = dd[1] * i + dd[1] / 2
                        inum += 1

                if array[-1, j, k]:
                    xf[inum, j, k] = lx + dd[0]

        return xi, xf

    elif dim == 'y':
        yi = np.zeros((nobjmax, shape[0], shape[2]))
        yf = np.zeros((nobjmax, shape[0], shape[2]))

        for k in range(shape[2]):
            for i in range(shape[0]):
                jnum = 0
                if array[i, 1, k]:
                    yi[jnum, i, k] = -dd[2]

                for j in range(shape[1] - 1):
                    if not array[i, j, k] and array[i, j + 1, k]:
                        yi[jnum, i, k] = dd[3] * j + dd[3] / 2
                    elif array[i, j, k] and not array[i, j + 1, k]:
                        yf[jnum, i, k] = dd[3] * j + dd[3] / 2
                        jnum += 1

                if array[i, -1, k]:
                    yf[jnum, i, k] = ly + dd[2]

        return yi, yf

    else:
        zi = np.zeros((nobjmax, shape[0], shape[1]))
        zf = np.zeros((nobjmax, shape[0], shape[1]))

        for j in range(shape[1]):
            for i in range(shape[0]):
                knum = 0
                if array[i, j, 1]:
                    zi[knum, i, j] = -dd[4]

                for k in range(shape[2] - 1):
                    if not array[i, j, k] and array[i, j, k + 1]:
                        zi[knum, i, j] = dd[5] * k + dd[5] / 2
                    elif array[i, j, k] and not array[i, j, k + 1]:
                        zf[knum, i, j] = dd[5] * k + dd[5] / 2
                        knum += 1

                if array[i, j, -1]:
                    zf[knum, i, j] = ly + dd[4]

        return zi, zf
