import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.zip.ZipInputStream;

public class MinecraftModDownloaderMacOS {

    @SuppressWarnings("deprecation")
    public static void main(String[] args) {
        String fileURL = "https://github.com/TogiFerretFerret/mods/releases/download/brrr'/mods.zip";
        String userHome = System.getProperty("user.home");
        Path minecraftPath = Paths.get(userHome, "Library", "Application Support", "minecraft");
        Path zipPath = minecraftPath.resolve("mods.zip");

        try {
            // Create the minecraft directory if it doesn't exist
            if (!Files.exists(minecraftPath)) {
                Files.createDirectories(minecraftPath);
                System.out.println("Created minecraft directory.");
            }

            // Download the file with a progress bar
            System.out.println("Downloading mods.zip...");
            URL url = new URL(fileURL);
            HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();
            long completeFileSize = httpConnection.getContentLengthLong();

            try (InputStream inputStream = httpConnection.getInputStream();
                 FileOutputStream fileOutputStream = new FileOutputStream(zipPath.toFile())) {

                byte[] buffer = new byte[4096];
                long downloadedFileSize = 0;
                int bytesRead;

                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    fileOutputStream.write(buffer, 0, bytesRead);
                    downloadedFileSize += bytesRead;
                    printProgressBar(downloadedFileSize, completeFileSize);
                }
            }
            System.out.println("\nDownload complete.");


            // Unzip the file
            System.out.println("Unzipping mods.zip...");
            try (ZipInputStream zis = new ZipInputStream(Files.newInputStream(zipPath))) {
                var zipEntry = zis.getNextEntry();
                while (zipEntry != null) {
                    Path newPath = minecraftPath.resolve(zipEntry.getName()).normalize();
                    // This is a security check to prevent Zip Slip vulnerability
                    if (!newPath.startsWith(minecraftPath)) {
                        throw new IOException("Zip entry is outside of the target dir: " + zipEntry.getName());
                    }

                    if (zipEntry.isDirectory()) {
                        Files.createDirectories(newPath);
                    } else {
                        if (newPath.getParent() != null) {
                            if (Files.notExists(newPath.getParent())) {
                                Files.createDirectories(newPath.getParent());
                            }
                        }
                        // Use a buffer to write the file
                        try (FileOutputStream fos = new FileOutputStream(newPath.toFile())) {
                            byte[] innerBuffer = new byte[1024];
                            int len;
                            while ((len = zis.read(innerBuffer)) > 0) {
                                fos.write(innerBuffer, 0, len);
                            }
                        }
                    }
                    zipEntry = zis.getNextEntry();
                }
                zis.closeEntry();
            }
            System.out.println("Unzipping complete.");

            // Clean up the downloaded zip file
            Files.delete(zipPath);
            System.out.println("Deleted mods.zip.");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private static void printProgressBar(long downloaded, long total) {
        int percent = (int) ((downloaded * 100) / total);
        StringBuilder bar = new StringBuilder("[");
        int barWidth = 50; // Width of the progress bar in characters
        for (int i = 0; i < barWidth; i++) {
            if (i < barWidth * percent / 100) {
                bar.append("=");
            } else if (i == barWidth * percent / 100) {
                bar.append(">");
            } else {
                bar.append(" ");
            }
        }
        bar.append("] ").append(percent).append("%");
        System.out.print("\r" + bar.toString());
    }
}
