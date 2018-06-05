import alpr
import sqlite3

def main():
    reserve = []
    time = 1
    while(True):
        print(f"current time: {time}")
        print("========Please enter command==========")
        cmd = input()
        # cmd = "IN_CAPTURE lot1"
        # cmd = "OUT_CAPTURE lot1"
        re = cmd.split(' ')
        if(re[0]=="IN_CAPTURE"):
            plate = alpr.cap()
            print("====Enter: "+plate)
            # time = re[2]
            lot_name = re[1]
            if plate in reserve:
                conn = sqlite3.connect('pk_user.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE user_list  SET in_time = ? WHERE plate = ?",(time, plate,))
                cursor.execute("SELECT * FROM user_list WHERE plate = ?",(plate,))
                print(f"--{plate} enter at time {time}")
                print(cursor.fetchone())
                conn.commit()
                conn.close()
            else:
                conn = sqlite3.connect('pk.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pk_list WHERE pk_name = ?",(lot_name,))
                temp = cursor.fetchone()
                new_occ = temp[1]+1
                if(temp[2]!=new_occ):
                    print(f"--Lot {lot_name} enter 1 car.")
                    print("--New_occ: "+str(new_occ))
                    cursor.execute("UPDATE pk_list  SET occ = ? WHERE pk_name = ?",(new_occ, lot_name,))

                    cursor.execute("SELECT * FROM pk_list WHERE pk_name = ?",(lot_name,))
                    print(cursor.fetchone())

                    conn.commit()
                    conn.close()

                    conn = sqlite3.connect('pk_user.db')
                    cursor = conn.cursor()
                    cursor.execute("UPDATE user_list  SET in_time = ? WHERE plate = ?",(time, plate,))
                    cursor.execute("SELECT * FROM user_list WHERE plate = ?",(plate,))
                    print(f"--{plate} enter at time {time}")
                    print(cursor.fetchone())
                    conn.commit()
                    conn.close()
                else:
                    print(f"{lot_name} FULL")

        elif(re[0]=="OUT_CAPTURE"):
            plate = alpr.cap()
            print("====Leave: "+plate)
            lot_name = re[1]

            conn = sqlite3.connect('pk.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pk_list WHERE pk_name = ?",(lot_name,))
            temp = cursor.fetchone()
            new_occ = temp[1]-1

            print(f"--{lot_name} leave 1 car.")
            print("--New_occ: "+str(new_occ))
            cursor.execute("UPDATE pk_list  SET occ = ? WHERE pk_name = ?",(new_occ, lot_name,))
            cursor.execute("SELECT * FROM pk_list WHERE pk_name = ?",(lot_name,))
            print(cursor.fetchone())
            conn.commit()
            conn.close()

            conn = sqlite3.connect('pk_user.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_list WHERE plate = ?",(plate,))
            temp = cursor.fetchone()
            ch = charge_function(temp[4], int(time))
            new_wallet = temp[2]-ch

            cursor.execute("UPDATE user_list  SET in_time = 0 WHERE plate = ?",(plate,))
            cursor.execute("UPDATE user_list  SET wallet = ? WHERE plate = ?",(new_wallet ,plate,))

            cursor.execute("SELECT * FROM user_list WHERE plate = ?",(plate,))
            print(f"--{plate} leave at time {time}")
            print(f"--charged {ch}")
            print(cursor.fetchone())
            conn.commit()
            conn.close()

        elif(re[0]=="RESERVE"):#RESERVE plate lot1
            lot_name = re[2]
            plate = re[1]
            reserve.append(plate)
            conn = sqlite3.connect('pk.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pk_list WHERE pk_name = ?",(lot_name,))
            temp = cursor.fetchone()
            new_occ = temp[1]+1
            cursor.execute("UPDATE pk_list  SET occ = ? WHERE pk_name = ?",(new_occ, lot_name,))

            cursor.execute("SELECT * FROM pk_list WHERE pk_name = ?",(lot_name,))
            print(cursor.fetchone())

            conn.commit()
            conn.close()
        elif(re[0]=="pass"):
            pass
        time = time+1

def charge_function(intime, outtime):
    return outtime-intime

if __name__ == '__main__':
    main()
