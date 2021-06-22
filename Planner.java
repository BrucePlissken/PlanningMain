import JSHOP2.*;
import java.io.*;
import JSHOP2.Calculate;

class Planner implements Calculate {
    InternalDomain idomain;
    File file;
    //JSHOP2Parser parser;
    Planner(){
        file = new File("tmp/basic/basic");
        // parser = new JSHOP2Parser();
        start();
        
    }
    
    public Term call(List list){


        return list.getHead();
    }

    public void start(){
        
        //System.out.print( );
        
        try {
            idomain = new InternalDomain(file, 2);
            //idomain.parser.command();
            
        } catch (Exception e) {
            //TODO: handle exception
            System.out.println("exception " + e);
        }
    }        
        
       
        
        
        
    public static void main(String[] args) {
        
        new Planner();
    }
}