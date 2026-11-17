#import <Foundation/Foundation.h>
@implementation Tracker
- (NSTimeInterval)boot { return [[NSProcessInfo processInfo] systemUptime]; }
@end
