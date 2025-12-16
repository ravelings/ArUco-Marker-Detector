from Packages.calibrator import Calibrate

def main() -> None:
    file_path = 'images'
    diemension = (7,7)
    calibrate = Calibrate(board_diemension=diemension, folder_path=file_path)  
    calibrate.calibrateMatrix()
    print(f'Matrix: {calibrate.matrix}')
    
    print("Program ended")
    
if __name__ == "__main__":
    main()
