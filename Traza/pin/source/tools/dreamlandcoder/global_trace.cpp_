#include <iostream>
#include <fstream>
#include <utility>      // std::pair, std::make_pair
#include <string>       // std::string
#include "pin.H"
using std::cerr;
using std::ofstream;
using std::ios;
using std::string;
using std::cout;
using std::hex;
using std::flush;
using std::dec;
using std::endl;

std::map<long unsigned int, string> intrucctions_dissasembler;

//make obj-intel64/global_trace.so TARGET=intel64
//../../../pin -t obj-intel64/global_trace.so -- ~/Escritorio/C/TFG/Traza/jump_line_detect.o



ofstream outFile;
KNOB<string> KnobOutputFile(KNOB_MODE_WRITEONCE, "pintool",
    "o", "traza.out", "specify output file name");
bool flag_jump;


VOID Before(VOID *instr_addrs, VOID * jump_to_address, INT64 taken)
{
    
    outFile << intrucctions_dissasembler[(long unsigned int)instr_addrs]
    << ","
    << hex 
    << (unsigned long long)instr_addrs
    << ","
    << (unsigned long long) jump_to_address
    << ","
    << (unsigned long long)taken
    << endl;
    return;
}
VOID Instruction(INS ins, VOID *v)
{

    if (INS_IsBranch(ins))
    {
	std::pair <long unsigned int, string> entrie ((LEVEL_PINCLIENT::INS_Address(ins)), INS_Disassemble(ins));

	intrucctions_dissasembler.insert(entrie); 
        INS_InsertCall(ins,
                       IPOINT_BEFORE,
                       AFUNPTR(Before),
                       IARG_INST_PTR,
                       IARG_BRANCH_TARGET_ADDR,
                       IARG_BRANCH_TAKEN,
                       IARG_END);
        
    }
}

// This function is called when the application exits
VOID Fini(INT32 code, VOID *v)
{
    outFile.close();
}
INT32 Usage()
{
    cerr << "This tool dump heap memory information (global variable) ..." << endl;
    cerr << endl
         << KNOB_BASE::StringKnobSummary() << endl;
    return -1;
}
int main(int argc, char *argv[])
{
    flag_jump = 0;
    char * file_path;
    // Initialize pin
    if (PIN_Init(argc, argv))
        return Usage();

    file_path = getenv("FILE_PATH_TRAZA");
    
    if(file_path){
	    outFile.open(file_path);
    }
    else{
	    outFile.open(KnobOutputFile.Value().c_str());
    }
    

    
    
    outFile << dec << "instruccion"
    << ","
    << hex 
    << "address_src"
    << ","
    << "address_dts"
    << ","
    << "was_jump"
    << endl;
    // Register Instruction to be called to instrument instructions
    INS_AddInstrumentFunction(Instruction, 0);
    // Register Fini to be called when the application exits
    PIN_AddFiniFunction(Fini, 0);
    // Start the program, never returns
    PIN_StartProgram();
    return 0;
}
