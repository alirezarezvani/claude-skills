import UIKit
import AVFoundation

final class Settings {
    func lastSync() -> Date? { UserDefaults.standard.object(forKey: "lastSync") as? Date }
    func uptime() -> TimeInterval { ProcessInfo.processInfo.systemUptime }
    func cacheAge(_ url: URL) throws -> Date? {
        try FileManager.default.attributesOfItem(atPath: url.path)[.modificationDate] as? Date
    }
    func scanBarcode() { _ = AVCaptureDevice.default(for: .video) }
}
