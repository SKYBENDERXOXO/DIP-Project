#Assignment PH401 1901EE69

import matplotlib.pyplot as plt


def cu_octa_total(k):
    ans = (10*(k**3) + 15*(k**2) + 11*k + 3)/3
    return ans


def cu_octa_surf(k):
    ans = 10*(k**2) + 2
    return ans


def sph_total(k):
    ans = (10*(k**3) - 15*(k**2) + 11*k - 3)/3
    return ans


def sph_surface(k):
    ans = 10*(k**2) + 12 - 20*k
    return ans


def main():

    option = input("Press 1-> CuboOctahedral , 2-> Spherical: ")
    
    try:
        option = int(option)
    except:
        print("Invalid Input!")
        return

    if not (option == 1 or option == 2):
        print("Invalid Input")
        return
    
    atoms_surface = []
    atoms_bulk = []
    sizes_of_particle = [i + 1 for i in range(50)]

#Calculation of surface and bulk atoms
    for particle_size in sizes_of_particle:
        if option == 1:
            x = (cu_octa_surf(particle_size) /
                    cu_octa_total(particle_size))*100
        else:
            x = (sph_surface(particle_size) /
                    sph_total(particle_size))*100

        atoms_surface.append(x)
        atoms_bulk.append(100 - x)

#Graph plotting 
    plt.scatter(sizes_of_particle, atoms_bulk, label="bulk atoms")
    plt.scatter(sizes_of_particle, atoms_surface, label="surface atoms")
    plt.legend(loc='center right')
    plt.xlabel("particle size")
    plt.ylabel("% of atoms in bulk/surface")
    if option == 1:
        plt.title("CuboOctahedral")
    else:
        plt.title("Spherical")
    plt.show()


if __name__ == "__main__":
    main()