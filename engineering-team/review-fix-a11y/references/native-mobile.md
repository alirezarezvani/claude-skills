# Native Mobile Accessibility Reference

This skill primarily targets **web and mobile web**. For native mobile apps, the same principles apply (labels, focus order, semantics, contrast) but the APIs differ. Use this reference when working with React Native, iOS (Swift/UIKit), or Android.

## React Native

### Key APIs

| What | API |
|------|-----|
| Label | `accessibilityLabel="Description"` |
| Hint | `accessibilityHint="Double tap to activate"` |
| Role | `accessibilityRole="button"` / `"link"` / `"header"` / `"image"` / `"none"` |
| State | `accessibilityState={{ disabled: true, selected: false, expanded: false }}` |
| Value | `accessibilityValue={{ min: 0, max: 100, now: 42 }}` |
| Live region | `accessibilityLiveRegion="polite"` / `"assertive"` |
| Hidden from AT | `importantForAccessibility="no-hide-descendants"` (Android) |
| Element grouping | `accessible={true}` on parent to group children |

### Example: Accessible Button

```jsx
<TouchableOpacity
  accessibilityLabel="Submit order"
  accessibilityRole="button"
  accessibilityState={{ disabled: isLoading }}
  onPress={handleSubmit}
>
  <Text>Submit</Text>
</TouchableOpacity>
```

### Example: Header

```jsx
<Text accessibilityRole="header">Account Settings</Text>
```

### Testing
- **iOS**: Enable VoiceOver in Simulator → Settings → Accessibility
- **Android**: Enable TalkBack in Emulator → Settings → Accessibility

---

## iOS (Swift / UIKit)

### Key Properties

| What | Property |
|------|----------|
| Label | `accessibilityLabel` |
| Hint | `accessibilityHint` |
| Value | `accessibilityValue` |
| Traits | `accessibilityTraits` (`.button`, `.link`, `.header`, `.image`, `.selected`, `.notEnabled`) |
| Is element | `isAccessibilityElement = true/false` |
| Frame | `accessibilityFrame` (for custom hit areas) |
| Grouping | `shouldGroupAccessibilityChildren = true` on container |

### Example

```swift
button.accessibilityLabel = "Submit order"
button.accessibilityTraits = .button
button.accessibilityHint = "Double tap to complete purchase"
```

### Announcements

```swift
UIAccessibility.post(notification: .announcement, argument: "Order submitted")
UIAccessibility.post(notification: .screenChanged, argument: mainContentView)
```

### Testing
- Xcode: Product → Profile → Accessibility Inspector
- Device/Simulator: Settings → Accessibility → VoiceOver

---

## Android

### Key APIs

| What | API |
|------|-----|
| Description | `android:contentDescription` |
| Hide from AT | `android:importantForAccessibility="no"` |
| Live region | `android:accessibilityLiveRegion="polite"` / `"assertive"` |
| Custom node | Override `onInitializeAccessibilityNodeInfo()` in custom views |
| Announce | `view.announceForAccessibility("Message")` |

### Example (XML)

```xml
<ImageButton
    android:contentDescription="@string/submit_order"
    android:importantForAccessibility="yes" />
```

### Example (Kotlin)

```kotlin
binding.submitButton.contentDescription = "Submit order"
binding.submitButton.announceForAccessibility("Order submitted successfully")
```

### Testing
- Android Studio: Accessibility Scanner app
- Device: Settings → Accessibility → TalkBack

---

## Cross-Platform Checklist

- [ ] Every interactive element has a label (not just visual text inside)
- [ ] Roles match element behavior (button, link, header, image)
- [ ] Disabled state communicated via `accessibilityState`/`isEnabled`
- [ ] Dynamic content updates announced via live region or `announceForAccessibility`
- [ ] Focus order follows logical/visual order (avoid random `focusable` ordering)
- [ ] Color contrast ≥4.5:1 for text, ≥3:1 for UI components (same as web)
- [ ] Touch targets ≥44×44pt (iOS) / ≥48×48dp (Android)
- [ ] Tested with VoiceOver (iOS) and TalkBack (Android)
