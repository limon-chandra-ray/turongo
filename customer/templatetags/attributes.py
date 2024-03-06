from django import template

register = template.Library()

def addClass(value,token):
    value.field.widget.attrs["class"] = token
    return value
def addPlaceholder(value,token):
    value.field.widget.attrs["placeholder"] = token
    return value

def addCols(value,token):
    value.field.widget.attrs['cols'] = token
    return value

def addRows(value,token):
    value.field.widget.attrs['rows'] = token
    return value
def minLength(value,token):
    value.field.widget.attrs['minlength'] =  token
    return value

register.filter(addClass)
register.filter(addPlaceholder) 
register.filter(addCols)
register.filter(addRows)
register.filter(minLength)