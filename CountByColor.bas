Attribute VB_Name = "Module1"
Function CountByColor(DataRange As Range, ColorSample As Range) As Long
    Dim cell As Range, n As Long
     
    For Each cell In DataRange
        If cell.Interior.Color = ColorSample.Interior.Color Then n = n + 1
    Next cell
    CountByColor = n
End Function
