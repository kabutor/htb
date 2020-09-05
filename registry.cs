// COMPILE AS
// c:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe -out:registry.exe registry.cs
// USE AS
// registry SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run

using System;
using System.Security.AccessControl;
using System.Security.Principal;
using System.Security;
using Microsoft.Win32;
using System.Linq;

public class Program
{
	public static void Main(string[] args)
	{
        if (args.Length < 1)
        {
            Console.WriteLine("No Args");
            System.Environment.Exit(1);
        }
        else
        {
            Console.WriteLine(args[0]);
        }

        RegistryKey key = Registry.LocalMachine.OpenSubKey(args[0]);
        RegistrySecurity security = key.GetAccessControl();


        foreach (RegistryAccessRule rule in security.GetAccessRules(true, true, typeof(System.Security.Principal.NTAccount)))
            {
            if (rule.InheritanceFlags.ToString() == "None")
            {
                Console.WriteLine("        User: {0}", rule.IdentityReference);
                Console.WriteLine("        Type: {0}", rule.AccessControlType);
                Console.WriteLine("      Rights: {0}", rule.RegistryRights);
                //Console.WriteLine(" Inheritance: {0}", rule.InheritanceFlags);
                //Console.WriteLine(" Propagation: {0}", rule.PropagationFlags);
                //Console.WriteLine("   Inherited? {0}", rule.IsInherited);
                Console.WriteLine();
            }
            }
        
	}
}