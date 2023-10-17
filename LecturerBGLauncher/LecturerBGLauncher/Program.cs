using System.Diagnostics;

public static class Program
{
    private static int lastHour = -1;
    
    public static void Main(string[] args)
    {
        Console.WriteLine("lecturer bg pog");
        DoTheThing();
        System.Timers.Timer timer = new(TimeSpan.FromMinutes(1));
        timer.Elapsed += (sender, eventArgs) =>
        {
            DoTheThing();
        };
        timer.Start();
        
        while (true)
            Thread.Sleep(100000); // lmao
    }

    public static void DoTheThing()
    {
        Console.WriteLine("running");
        int hour = DateTime.Now.Hour;
        if (lastHour != hour
            && hour is >= 9 and <= 21)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "python";
            start.Arguments = "main.py";
            start.UseShellExecute = false;
            start.CreateNoWindow = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start)!)
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    Console.Write(result);
                }
            }

            lastHour = hour;
        }
    }
}
