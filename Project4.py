def simulate(I,DIC,Cmulti,Cpipe, Memory):
    print("ECE366 Fall 2018 ISA Design: Simulator")
    print()
    PC = 0              # Program-counter
    DIC = 0
    Reg = [0,0,0,0,0,0,0,0]     # 7 registers, init to all 0
    print("******** Simulation starts *********")
    finished = False
    while(finished != True):
        fetch = I[PC]
        DIC += 1
        Cpipe += 1
        ending = 0
        if(fetch[0:6] == "100000"):
            #op = "add"
            Reg[fetch[6:11]] = Reg[fetch[11:16]] + Reg[fetch[16:21]]
            Cmulti += 3
            ending = 4
            PC +=1
        elif (fetch[0:6] == "001000"):
            #op = "addi"
            Reg[fetch[6:11]] = Reg[fetch[11:16]] + fetch[16:32]
            Cmulti += 4
            ending = 4
            PC +=1
        elif (fetch[0:6] == "100010"):
            #op = "sub"
            Reg[fetch[6:11]] = Reg[fetch[11:16]] - Reg[fetch[16:21]]
            Cmulti += 4
            ending = 4
            PC +=1
        elif (fetch[1:6] == "100110"):
            #op = "xor"
            Reg[fetch[6:11]] = Reg[fetch[11:16]] ^ Reg[fetch[16:21]]
            Cmulti += 4
            ending = 4
            PC +=1
        elif (fetch[0:6] == "000100"):
            #op = "beq"
            if(Reg[fetch[6:11]] == Reg[fetch[11:16]]):
                PC = PC + fetch[16:32]
            else:
                PC = PC + 1
            Cmulti += 3
            ending = 4
        elif (fetch[0:6] == "000101"):
            #op = "bne"
            if(Reg[fetch[6:11]] != Reg[fetch[11:16]]):
                PC = PC + fetch[16:32]
            else:
                PC = PC + 1
            Cmulti += 3
            ending = 4
        elif (fetch[0:6] == "101001"):
            #op = "slt"	
            if(Reg[fetch[11:16]] < Reg[fetch[16:21]]):
                Reg[fetch[6:11]] = 1
            else:
                Reg[fetch[6:11]] = 0
            PC += 1
            ending = 4
        elif (fetch[1:4] == "100011"):
            #op = "lw"
            Reg[fetch[6:11]] = Memory[Reg[11:16]] 
            PC += 1
            ending = 3

        elif (fetch[1:4] == "101011"):
            #op = "sw"
            Memory[Reg[fetch[11:16]]+Reg[fetch[16:32]]] = Reg[fetch[6:11]]
            PC +=1
            ending = 3
        
        
       
            
#        if(debug_mode):
#            if ( (DIC % Nsteps) == 0): # print stats every Nsteps
#                print("Registers R0-R3: ", Reg)
#                print("Program Counter : ",PC)
#                #print("Memory: ",Memory)   # Dont print memory atm. 
#                                            # Too much cluster
#                input("Press any key to continue")
#               print()
#        else:
#            continue
    if(ending == 3):
        Cpipe += 3
    else:
        Cpipe += 4
    print("******** Simulation finished *********")
    print("Dynamic Instr Count: ",DIC)
    print("Registers R0-R7: ",Reg)
    print("Cycles in Pipeline: ",Cpipe)
    print("Cycles in Multi-cycle CPU: ",Cmulti)
                                                              
    

    data.close()
        
def main():
    instr_file = open("1A.txt","r") #this is the machine code that has the instructions for prog 1
    mem_file = open("Memory.txt","r")
    #debug_mode = False  # is machine in debug mode?   
    Instruction = []    # all instructions will be stored here
    Memory = []
    DIC = 0
    Cmulti = 0
    Cpipe = 0
    #Simulation                       
    for line in instr_file: # Read in instr 
        if (line == "\n" or line[0] =='#'):              # empty lines,comments ignored
            continue
        line = line.replace("\n","")                                                      
        line = bin(line)
        Instruction.append(line)                        # Copy all instruction into a list
    for line in mem_file:
        if(line == "\n" or line[0] =='#'):
            continue
        line = line.replace("\n","")
        line = bin(line)
        Memory.append(line)
    simulate(Instruction,DIC,Cycles,Memory)
    
    #instr_file.close()
    #data_file.close()
    
if __name__ == "__main__":
    main()  
