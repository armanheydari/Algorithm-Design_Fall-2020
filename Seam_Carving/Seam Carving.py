from PIL import Image
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from os import path


class SeamCarving:
    name = input("please type the path of image: ")
    mainImage = Image.open(name)
    name = name.split("\\")
    name = name[len(name)-1].split('.')[0]
    width, height = mainImage.size
    print('your photo size is', width, '*', height)
    verticals = int(input('how many vertical seams do you want to remove? '))
    horizontals = int(input('how many horizontal seams do you want to remove? '))
    image = np.array(mainImage)
    energy_photo = image.copy()
    energies = []
    variables = image.shape[2]

    def main(self):
        print('start')
        if not path.exists(f'.\outputs'):
            os.mkdir(f'.\outputs')
        if not path.exists(f'.\outputs\\{self.name}'):
            os.mkdir(f'.\outputs\\{self.name}')
        if self.verticals > 0:
            maximum_energy = 0
            for i in range(0, self.height - 1):
                temp = []
                for j in range(0, self.width - 1):
                    temp.append(self.Calculate_Energy(i, j))
                maximum_energy = max(max(temp), maximum_energy)
                self.energies.append(temp)
            self.Create_Energy_Picture(maximum_energy)
            for i in range(self.verticals):
                self.Remove_Seam(self.Find_Vertical_Seam())
                print(i+1, 'vertical seam')
        if self.horizontals > 0:
            plt.imsave('help energy photo.png', self.energy_photo.astype(np.uint8))
            plt.imsave('help output photo.png', self.image.astype(np.uint8))
            self.mainImage = Image.open('.\help output photo.png').rotate(90, expand=True)
            self.image = np.array(self.mainImage)
            self.width, self.height = self.mainImage.size
            self.energy_photo = np.array(Image.open('.\help energy photo.png').rotate(90, expand=True))
            os.remove('help output photo.png')
            os.remove('help energy photo.png')
            self.variables = self.image.shape[2]
            maximum_energy = 0
            self.energies = []
            for i in range(0, self.height - 1):
                temp = []
                for j in range(0, self.width - 1):
                    temp.append(self.Calculate_Energy(i, j))
                maximum_energy = max(max(temp), maximum_energy)
                self.energies.append(temp)
            if self.verticals == 0:
                self.Create_Energy_Picture(maximum_energy)
                temp = Image.open(f".\outputs\\{self.name}\\energy photo.png")
                temp.rotate(270, expand=True).save(f".\outputs\\{self.name}\\energy photo.png")
            for i in range(self.horizontals):
                self.Remove_Seam(self.Find_Vertical_Seam())
                print(i + 1, 'horizontal seam')
            plt.imsave('help energy photo.png', self.energy_photo.astype(np.uint8))
            temp = Image.open(".\help energy photo.png")
            temp.rotate(270, expand=True).save(f".\outputs\\{self.name}\\removed seams.png")
            os.remove('help energy photo.png')
            plt.imsave('help output photo.png', self.image.astype(np.uint8))
            temp = Image.open(".\help output photo.png")
            temp.rotate(270, expand=True).save(f".\outputs\\{self.name}\\result.png")
            os.remove('help output photo.png')
        else:
            plt.imsave(f".\outputs\\{self.name}\\removed seams.png", self.energy_photo.astype(np.uint8))
            plt.imsave(f".\outputs\\{self.name}\\result.png", self.image.astype(np.uint8))
        print(f'successfully saved in outputs folder in', self.name)

    def Calculate_Energy(self, x, y):
        R1x = int(self.image[x + 1, y][0])
        G1x = int(self.image[x + 1, y][1])
        B1x = int(self.image[x + 1, y][2])
        R2x = int(self.image[x - 1, y][0])
        G2x = int(self.image[x - 1, y][1])
        B2x = int(self.image[x - 1, y][2])
        Rx = R1x - R2x
        Gx = G1x - G2x
        Bx = B1x - B2x
        deltaX = Rx * Rx + Gx * Gx + Bx * Bx
        R1y = int(self.image[x, y + 1][0])
        G1y = int(self.image[x, y + 1][1])
        B1y = int(self.image[x, y + 1][2])
        R2y = int(self.image[x, y - 1][0])
        G2y = int(self.image[x, y - 1][1])
        B2y = int(self.image[x, y - 1][2])
        Ry = R1y - R2y
        Gy = G1y - G2y
        By = B1y - B2y
        deltaY = Ry * Ry + Gy * Gy + By * By
        energy = math.sqrt(deltaX + deltaY)
        return energy

    def Create_Energy_Picture(self, maximum_energy):
        rate = 255 / maximum_energy
        for i in range(0, self.height - 2):
            for j in range(0, self.width - 2):
                temp = int(self.energies[i][j] * rate)
                if self.variables == 4:
                    self.energy_photo[i, j] = (temp, temp, temp, 255)
                else:
                    self.energy_photo[i, j] = (temp, temp, temp)
        plt.imsave(f'.\outputs\\{self.name}\\energy photo.png', self.energy_photo.astype(np.uint8))

    def Find_Vertical_Seam(self):
        minimum_path = [100000000, []]
        for i in range(1, self.width - 3):
            seam = [0, [(0, i)]]
            temp = i
            for j in range(1, self.height - 1):
                if temp == 0:
                    if self.energies[j][temp + 1] < self.energies[j][temp]:
                        seam[0] += self.energies[j][temp + 1]
                        seam[1].append((j, temp + 1))
                        temp += 1
                    else:
                        seam[0] += self.energies[j][temp]
                        seam[1].append((j, temp))
                elif temp == self.width - 3:
                    if self.energies[j][temp - 1] < self.energies[j][temp]:
                        seam[0] += self.energies[j][temp - 1]
                        seam[1].append((j, temp - 1))
                        temp -= 1
                    else:
                        seam[0] += self.energies[j][temp]
                        seam[1].append((j, temp))
                else:
                    if self.energies[j][temp - 1] < self.energies[j][temp] and self.energies[j][temp - 1] < \
                            self.energies[j][temp + 1]:
                        seam[0] += self.energies[j][temp - 1]
                        seam[1].append((j, temp - 1))
                        temp -= 1
                    elif self.energies[j][temp + 1] < self.energies[j][temp - 1] and self.energies[j][temp + 1] < \
                            self.energies[j][temp]:
                        seam[0] += self.energies[j][temp + 1]
                        seam[1].append((j, temp + 1))
                        temp += 1
                    else:
                        seam[0] += self.energies[j][temp]
                        seam[1].append((j, temp))
            if minimum_path[0] >= seam[0]:
                minimum_path = seam
        self.width -= 1
        return minimum_path[1]

    def Remove_Seam(self, remove_path):
        if self.variables == 4:
            temp = self.image.tolist()
            for index in remove_path:
                self.energy_photo[index[0], index[1]] = [255, 0, 0, 255]
                temp[index[0]][index[1]] = -1
                self.energies[index[0]][index[1]] = -1
        else:
            temp = self.image.tolist()
            for index in remove_path:
                self.energy_photo[index[0], index[1]] = [255, 0, 0]
                temp[index[0]][index[1]] = -1
                self.energies[index[0]][index[1]] = -1
        for row in self.energies:
            while -1 in row:
                row.remove(-1)
        for row in temp:
            if -1 in row:
                row.remove(-1)
            else:
                row.pop(0)
        self.width -= 1
        self.image = np.array(temp)


if __name__ == "__main__":
    SeamCarving().main()
