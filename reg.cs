using System.Security.Permissions;
using System.Security;
using Microsoft.Win32;
using System;
using System.Security.AccessControl;

public class Program
{
	public static void Main(string[] args)
	{

        if (args.Length < 1) 
        {
            Console.WriteLine("No Args");
	    System.Environment.Exit(1);
        }else{
		Console.WriteLine(args[0]);
		}
        try
        {
		//RegistryKey rk = Registry.CurrentUser;
		RegistryKey rk2;
		rk2= Registry.LocalMachine.OpenSubKey(args[0], true);
		rk2.Close();
		Console.WriteLine("true");
        }
	        catch (SecurityException)
        {
            Console.WriteLine("false");
        }
	
    }

}