import java.io.*;
import java.util.*;

/**
 * Log file analyzer
 * Map<processName, Map<dateTime, descriptions>>
 */
public class LogAnalyzer {
    private Map<String, Map<String, List<String>>> processToDateList;

    /**
     * process a log file and store data to a Map
     *
     * @param filenames the array of file names to analyze
     */
    public LogAnalyzer(String[] filenames) {
        processToDateList = new HashMap<>();
        try {
            for (String filename : filenames) {
                File inputFile = new File(filename);
                BufferedReader reader = new BufferedReader(new FileReader(inputFile));
                String currentLine = reader.readLine();

                while (currentLine != null) {
                    if (currentLine.length() == 0) continue;
                    String[] T = currentLine.split("\\s", 6);
                    String dateTimeString = T[0] + " " + T[1] + " " + T[2];
                    String process = T[4];
                    String description = T[5];

                    Map<String, List<String>> dateToDescription = processToDateList.get(process);
                    if (dateToDescription != null) {
                        List<String> descriptionList = dateToDescription.get(dateTimeString);
                        if (descriptionList != null) {
                            descriptionList.add(description);
                        } else {
                            descriptionList = new ArrayList<String>();
                            descriptionList.add(description);
                            dateToDescription.put(dateTimeString, descriptionList);
                        }
                    } else {
                        processToDateList.put(process, new HashMap<>());
                        processToDateList.get(process).put(dateTimeString, new ArrayList<String>());
                        processToDateList.get(process).get(dateTimeString).add(description);
                    }
                    currentLine = reader.readLine();
                }
                reader.close();
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            for (String key : processToDateList.keySet()) System.out.println(key);
        }
    }

    /**
     * find logs using a term
     *
     * @param term the search term
     * @return findings
     */
    public List<String> search(String term) {
        List<String> findings = null;
        return findings;
    }

    /**
     * find logs generated on a specific day
     *
     * @param term the search term
     * @param date the date
     * @return findings
     */
    public List<String> search(String term, String date) {
        List<String> findings = null;
        return findings;
    }

    /**
     * find logs generated within a date range
     * @param term the search term
     * @param fromDate starting date
     * @param toDate ending date
     * @return findings
     */
    public List<String> search(String term, String fromDate, String toDate) {
        List<String> findings = null;
        return findings;
    }

    /**
     * find logs generated within a from a starting time to an ending time
     * @param term the search term
     * @param date the day
     * @param fromTime start time
     * @param toTime end time
     * @return findings
     */
    public List<String> search(String term, String date, String fromTime, String toTime) {
        List<String> findings = null;
        return findings;
    }

    /**
     * find logs generated within a date range with starting and ending time
     * @param term the search term
     * @param fromDate the starting date
     * @param toDate the ending date
     * @param fromTime beginning at this time on the starting date
     * @param toTime ending at this time on the ending date
     * @return findings
     */
    public List<String> search(String term, String fromDate, String toDate, String fromTime, String toTime) {
        List<String> findings = null;
        return findings;
    }

    /**
     * test
     * @param args args
     */
    public static void main(String[] args) {
        LogAnalyzer LA = new LogAnalyzer(new String[]{"syslog5.log"});
        // LA.search("term");
    }
}
