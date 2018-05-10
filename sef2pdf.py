import os
from fpdf import FPDF
import string

unitorder = []
unitorder.extend(["Foundations of the Torah","Human Dispositions","Torah Study","Foreign Worship and Customs of the Nations","Repentance"])
unitorder.extend(["Reading the Shema","Prayer and the Priestly Blessing","Tefillin, Mezuzah and the Torah Scroll","Fringes","Blessings","Circumcision","The Order of Prayer"])
unitorder.extend(["Sabbath","Eruvin","Rest on the Tenth of Tishrei","Rest on a Holiday","Leavened and Unleavened Bread","Shofar, Sukkah and Lulav","Sheqel Dues","Sanctification of the New Month","Fasts","Scroll of Esther and Hanukkah"])
unitorder.extend(["Marriage","Divorce","Levirate Marriage and Release","Virgin Maiden","Woman Suspected of Infidelity"])
unitorder.extend(["Forbidden Intercourse","Forbidden Foods","Ritual Slaughter"])
unitorder.extend(["Oaths","Vows","Nazariteship","Appraisals and Devoted Property"])
unitorder.extend(["Diverse Species","Gifts to the Poor","Heave Offerings","Tithes","Second Tithes and Fourth Year's Fruit","First Fruits and other Gifts to Priests Outside the Sanctuary","Sabbatical Year and the Jubilee"])
unitorder.extend(["The Chosen Temple","Vessels of the Sanctuary and Those who Serve Therein","Admission into the Sanctuary","Things Forbidden on the Altar","Sacrificial Procedure","Daily Offerings and Additional Offerings","Sacrifices Rendered Unfit","Service on the Day of Atonement","Trespass"])
unitorder.extend(["Paschal Offering","Festival Offering","Firstlings","Offerings for Unintentional Transgressions","Offerings for Those with Incomplete Atonement","Substitution"])
unitorder.extend(["Defilement by a Corpse","Red Heifer","Defilement by Leprosy","Those Who Defile Bed or Seat","Other Sources of Defilement","Defilement of Foods","Vessels","Immersion Pools"])
unitorder.extend(["Damages to Property","Theft","Robbery and Lost Property","One Who Injures a Person or Property","Murderer and the Preservation of Life"])
unitorder.extend(["Sales","Ownerless Property and Gifts","Neighbors","Agents and Partners","Slaves"])
unitorder.extend(["Hiring","Plaintiff and Defendant","Creditor and Debtor","Borrowing and Deposit","Inheritances"])
unitorder.extend(["The Sanhedrin and the Penalties within their Jurisdiction","Testimony","Rebels","Mourning","Kings and Wars"])
print("Total # of units that exist = " + str(len(unitorder)))

class Sefer:
    def __init__(self, name):
        self.name = name
    def __eq__(self, sefer):
        return self.name == sefer.name

class Unit:
    def __init__(self, name, path, sefer):
        self.name = name
        self.path = path
        self.sefer = sefer
    def __eq__(self, unit):
        return self.name == unit.name and self.sefer == unit.sefer
    def __gt__(self, unit):
        return unitorder.index(self.name) > unitorder.index(unit.name)

# Sefaria-Export-Mishneh-Torah/Mishneh Torah/Sefer []/Mishneh Torah, []/English/merged.txt
# If set, only one unit will be comiled to reduce time.
TEST = False

base = "Sefaria-Export-Mishneh-Torah/Mishneh Torah/"
print("\nLooking for Mishneh Torah in: " + base + "\n")

st = ""
units = []
done = False
for seferfilename in os.listdir(base):
    if done:
        break
    if "Sefer" in seferfilename:
        sefer = Sefer(seferfilename)
        st += (seferfilename + "\n")
        for unitfilename in os.listdir(base + seferfilename + "/"):
            if done:
                break;
            if "Mishneh Torah" in unitfilename:
                path = (base + seferfilename + "/" + unitfilename + "/English/merged.txt")
                unit = Unit(unitfilename[15:], path, sefer)
                units.append(unit)
                st += ("  " + unitfilename[15:] + "\n")
                if TEST:
                    done = True
print(st)
print("Total # of units found = " + str(len(units)))

if not TEST:
    input("\nPress ENTER to compile a PDF\n> ENTER <")
print("")

allowed_chars = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"\'(),.:;/"

pdfname = "The_English_Yad.pdf"
typeface_normal = "Helvetica"
typeface_heading = typeface_normal

# Create pdf.
pdf = FPDF()
#pdf.add_font(typeface_normal, '', "C:/Windows/Fonts/" + typeface_normal + ".ttf", uni=True)
#pdf.add_font(typeface_normal, 'b', "C:/Windows/Fonts/" + typeface_normal + "b.ttf", uni=True)

margin = 12
pdf.set_auto_page_break(True, margin * (7.0 / 10.0))
pdf.set_left_margin(margin)
pdf.set_right_margin(margin)

# Title Page.
pdf.add_page()
pdf.set_font(typeface_heading, '', 45)
pdf.write(20, "\n\n\n\n\n\t\t\t\t\t\t\t The English Yad")

# TODO: Add PDF index:

unitsnotfound = 0
errors = ""

currentsefer = None

units = sorted(units)
for unit in units:
    try:
        with open(unit.path, "r", encoding="utf8") as english:
            unittext = english.read()

            # Heading, sefer title.
            if currentsefer is None or currentsefer != unit.sefer:
                # We are on a new sefer!
                print("Now compiling: " + unit.sefer.name)
                # New page for each Sefer.
                pdf.add_page()
                pdf.set_font(typeface_heading, 'BI', 22)
                pdf.write(3, "\n" + unit.sefer.name + "\n\n\n\n")
            currentsefer = unit.sefer

            # Heading, unit title.
            heading = unit.name+ "\n\n"
            pdf.set_font(typeface_heading, '', 17)
            pdf.write(5, heading)

            # Prepare for main text.
            text = ""

            # Skip all the BLAH at the beginning of each unit.
            startindex = unittext.index("Chapter")
            unittext = "+\n" + unittext[startindex:]

            just_newline = False
            open_angle = 0
            while len(unittext) > 0:
                char = unittext[0]
                if unittext.startswith("+\nChapter"):
                    pdf.set_font(typeface_normal, '', 10)
                    pdf.write(5, text)
                    # Find the whole chapter line.
                    chapline = unittext.split("\n")[1]
                    pdf.set_font(typeface_normal, 'B', 10)
                    pdf.write(5, chapline)
                    # Skip chapter line.
                    unittext = "\n" + unittext[2+len(chapline):]
                    just_newline = False
                elif char == "\n" and not just_newline:
                    pdf.set_font(typeface_normal, '', 10)
                    pdf.write(5, text)
                    pdf.write(4, "\n\n")
                    text = ""
                    just_newline = True
                    unittext = "+" + unittext[1:]
                else:
                    if char in "<":
                        open_angle += 1
                    elif char in ">":
                        open_angle -= 1
                        open_angle = max(open_angle, 0)
                    elif char in allowed_chars and open_angle == 0:
                        text += char
                        just_newline = False
                    unittext = unittext[1:]

            pdf.set_font(typeface_normal, '', 10)
            pdf.write(5, text)
    except FileNotFoundError:
        unitsnotfound += 1
        errors += ("No English found for: " + unit.name + "\n")

print("\n" + errors)
print("# of units English not found = " + str(unitsnotfound))
print("\nCompiling PDF...")
pdf.output(pdfname, "F")
print("--- Compiled " + str(len(units) - unitsnotfound) + " units ---\nDone, enjoy! Saved as: " + pdfname)
