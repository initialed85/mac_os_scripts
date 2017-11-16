on run argv

  tell application "System Events"

    set monitors to a reference to every desktop
    set numMonitors to count (monitors)

    repeat with monitorIndex from 1 to numMonitors by 1
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 1
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 2
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 3
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 4
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 5
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 6
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 7
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 8
    end repeat

  end tell

end run
