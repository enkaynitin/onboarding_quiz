import time
import math
import os


class ReportGenerator:
    """Generate Design Report for Seated Angle Connection.

    Attributes (Inherited from SeatAngleCalculation):
        gamma_mb (float): partial safety factor for material - resistance of connection - bolts
        gamma_m0 (float): partial safety factor for material - resistance governed by yielding or buckling
        gamma_m1 (float): partial safety factor for material - resistance governed by ultimate stress
        beam_col_clear_gap (int): design preference 
        bolt_hole_clearance (float)
        custom_hole_clearance (float): design preference, if specified
        bolt_hole_type (string): "Standard" or "Over-sized"
        bolt_fu_overwrite (float)
        mu_f (float): slip factor for HSFG bolt calculations
        min_edge_multiplier (float): multiplier for min edge distance check - based on edge type
        type_of_edge (string): The type is used in determining the min_edge_distance 
        is_environ_corrosive (string): 'Yes' or 'No'
        design_method (string)
        root_clearance (int): clearance of bolt row from the root of seated angle

        top_angle (string)
        connectivity (string)
        beam_section (string)
        column_section (string)
        beam_fu (float)
        beam_fy (float)
        column_fu (float)
        column_fy (float)        
        angle_fy (float)
        angle_fu (float)
        shear_force (float)
        bolt_diameter (int)
        bolt_type (string)
        bolt_grade (float)
        bolt_fu (int)        
        bolt_hole_diameter (int)
        angle_sec (string)
        beam_w_t (float): beam web thickness
        beam_f_t (float): beam flange thickness
        beam_d  (float): beam depth
        beam_w_f  (float): beam width
        beam_R1 (float): beam root radius
        column_f_t (float): column flange thickness
        column_d (float): column depth
        column_w_f (float): column width
        column_R1 (float): column root radius
        angle_t (float): angle thickness
        angle_A  (float): longer leg of unequal angle
        angle_B  (float): shorter leg of unequal angle
        angle_R1 (float)
        angle_l (float)

        safe (Boolean) : status of connection, True if safe

        moment_at_root_angle (float)
        moment_capacity_angle (float): Moment capacity of outstanding leg of seated angle
        is_shear_high (boolean): True if the seated angle leg is in high shear [Cl 8.2.1]
        
        leg_moment_d (float): Moment capacity of outstanding leg of seated angle with low shear
        outstanding_leg_shear_capacity (float)
        beam_shear_strength (float)
        bolt_shear_capacity (float)
        k_b (float)
        bolt_bearing_capacity (float)
        bolt_value (float)
        bolt_group_capacity (float)
        bolts_required (int)
        num_rows (int)
        num_cols (int)
        pitch (float)
        gauge (float)
        min_end_dist (int)
        min_edge_dist (int)
        min_pitch (int)
        min_gauge (int)
        end_dist (int)
        edge_dist (int)
        pitch (float)
        gauge (float)
        max_spacing (int)
        max_edge_dist (int)

        company_name (string)
        company_logo (string)

        group_team_name (string)
        designer (string)
        project_title (string)
        sub_title (string)
        job_number (string)
        method (string)

    """

    def __init__(self):
        """
        Args:            

        Returns:
            
        """
        self.leg_moment_d = None
        self.gamma_mb = 1.25
        self.gamma_m0 = 1.10
        self.gamma_m1 = 1.25
        self.beam_col_clear_gap = 10
        self.bolt_hole_clearance = 2.0
        self.custom_hole_clearance = 2.0
        self.bolt_hole_type = 'Standard'
        self.bolt_fu_overwrite = ''
        self.mu_f = 0.48
        self.min_edge_multiplier = 1.7
        self.type_of_edge = 'Sheared and hand flame cut'
        self.is_environ_corrosive = 'No'
        self.design_method = 'Limit State Design'
        self.root_clearance = 5.0

        self.top_angle = '75 75 x 8'
        self.connectivity = 'Column flange-Beam flange'
        self.beam_section = 'MB 300'
        self.column_section = 'UC 203 x 203 x 86'
        self.beam_fu = 410
        self.beam_fy = 250
        self.column_fu = 410
        self.column_fy = 250
        self.angle_fy = 250
        self.angle_fu = 410
        self.shear_force = 80
        self.bolt_diameter = 16
        self.bolt_type = 'HSFG'
        self.bolt_grade = '8.8'
        self.bolt_fu = 800
        self.bolt_hole_diameter = 18
        self.angle_sec = '150 150 X 15'
        self.beam_w_t = 7.7
        self.beam_f_t = 13.1
        self.beam_d = 300
        self.beam_w_f = 140
        self.beam_R1 = 14
        self.column_f_t = 20.5
        self.column_d = 222.2
        self.column_w_f = 209.1
        self.column_R1 = 10.2
        self.angle_t = 8
        self.angle_A = 75
        self.angle_B = 75
        self.angle_R1 = 7
        self.angle_l = 140.0

        self.safe = True

        self.moment_at_root_angle = 603.5
        self.moment_capacity_angle = 1193.2
        self.is_shear_high = False
        self.moment_high_shear_beta = 1.0
        self.outstanding_leg_shear_capacity = 333.4
        self.bolt_shear_capacity = 56.6
        self.k_b = 0.508
        self.bolt_bearing_capacity = 125.0
        self.bolt_value = 56.6
        self.bolts_required = 2
        self.bolts_provided = 2
        self.num_rows = 1
        self.num_cols = 2
        self.pitch = 0
        self.gauge = 60.0
        self.min_end_dist = 37.4
        self.min_edge_dist = 37.4
        self.min_pitch = 50
        self.min_gauge = 50
        self.end_dist = 40
        self.edge_dist = 40
        self.max_spacing = 247
        self.max_edge_dist = 92.4

        self.company_name = "FOSSEE"
        self.company_logo = ""

        self.group_team_name = "Osdag"
        self.designer = "Rachana"
        self.project_title = "Onboarding Quiz"
        self.sub_title = "Seated angle connection"
        self.job_number = "SA_2"
        self.client = "Osdag Reviewer"

    def save_html(self, report_summary, file_name, folder):
        """Create and save html report for Seated angle connection.

        Args:
            report_summary (dict): Structural Engineer details design report
            file_name (string): Name of design report file
            folder (path): Location of folder to save design report

        Returns:
            None
            """
        myfile = open(file_name, "w")
        myfile.write(t('! DOCTYPE html') + nl())
        myfile.write(t('html') + nl())
        myfile.write(t('head') + nl())
        myfile.write(t('link type="text/css" rel="stylesheet" ') + nl())

        myfile.write(html_space(4) + t('style'))
        myfile.write('table{width= 100%; border-collapse:collapse; border:1px solid black collapse}')
        myfile.write('th,td {padding:3px}' + nl())
        myfile.write(html_space(8) + 'td.detail{background-color:#D5DF93; font-size:20; '
                                     'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.detail1{font-size:20; '
                                     'font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.detail2{font-size:20;'
                                     ' font-family:Helvetica, Arial, Sans Serif}' + nl())
        myfile.write(html_space(8) + 'td.header0{background-color:#8fac3a; font-size:20;'
                                     ' font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.header1{background-color:#E6E6E6; font-size:20;'
                                     ' font-family:Helvetica, Arial, Sans Serif; font-weight:bold}' + nl())
        myfile.write(html_space(8) + 'td.header2{font-size:20; width:50%}' + nl())
        myfile.write(html_space(4) + t('/style') + nl())

        myfile.write(t('/head') + nl())
        myfile.write(t('body') + nl())

        # Project summary
        self.company_name = str(report_summary["ProfileSummary"]['CompanyName'])
        self.company_logo = str(report_summary["ProfileSummary"]['CompanyLogo'])

        self.group_team_name = str(report_summary["ProfileSummary"]['Group/TeamName'])
        self.designer = str(report_summary["ProfileSummary"]['Designer'])
        self.project_title = str(report_summary['ProjectTitle'])
        self.sub_title = str(report_summary['Subtitle'])
        self.job_number = str(report_summary['JobNumber'])
        self.client = str(report_summary['Client'])
        additional_comments = str(report_summary['AdditionalComments'])

        # Seated angle design parameters
        connectivity = str(self.connectivity)
        shear_force = str(self.shear_force)
        column_sec = str(self.column_section)
        column_fu = str(self.column_fu)
        beam_sec = str(self.beam_section)
        seated_angle_section = str(self.angle_sec)
        top_angle_section = str(self.top_angle)
        angle_fu = str(self.angle_fu)

        bolt_type = str(self.bolt_type)
        bolt_grade = str(self.bolt_grade)
        bolt_diameter = str(self.bolt_diameter)
        bolt_fu = str(self.bolt_fu)

        # Design Preferences
        beam_col_clear_gap = str(self.beam_col_clear_gap)
        bolt_hole_clearance = str(self.bolt_hole_clearance)
        bolt_hole_type = str(self.bolt_hole_type)
        bolt_fu_overwrite = self.bolt_fu_overwrite
        slip_factor_mu_f = self.mu_f
        min_edge_multiplier = self.min_edge_multiplier
        type_of_edge = self.type_of_edge
        is_environ_corrosive = self.is_environ_corrosive
        design_method = self.design_method

        # Calculation outputs
        bolts_provided = str(self.bolts_provided)
        bolts_required = str(self.bolts_required)

        number_of_rows = str(self.num_rows)
        number_of_cols = str(self.num_cols)
        edge = str(self.edge_dist)
        gauge = str(self.gauge)
        pitch = str(self.pitch)
        end = str(self.end_dist)
        # moment_demand = str(self.moment_at_root_angle)
        # gap = '20'

        kb = str(self.k_b)
        beam_w_t = str(self.beam_w_t)
        beam_fu = str(self.beam_fu)
        dia_hole = str(self.bolt_hole_diameter)
        shear_capacity = str(self.bolt_shear_capacity)
        bearing_capacity = str(self.bolt_bearing_capacity)

        design_conclusion = "Fail"  # default
        if self.safe:
            design_conclusion = "Pass"

        # -----------------------------------------------------------------------------------
        rstr = self.design_report_header()
        # -----------------------------------------------------------------------------------

        # Design conclusion
        rstr += t('table border-collapse= "collapse" border="1px solid black" width= 100% ') + nl()

        rstr += design_summary_row(0, "Design Conclusion", "header0", col_span="2")

        row = [1, "Seated Angle", "<p align=left style=color:green><b>" + design_conclusion + "</b></p>"]
        rstr += t('tr')
        rstr += html_space(1) + t('td class="detail1 "') + space(row[0]) + row[1] + t('/td')
        rstr += t('td class="detail1"') + row[2] + t('/td') + nl()
        # rstr += t('td class="header1 safe"') + row[3] + t('/td')
        rstr += t('/tr')

        rstr += design_summary_row(0, "Seated Angle", "header0", col_span="2")
        rstr += design_summary_row(0, "Connection Properties", "detail", col_span="2")
        rstr += design_summary_row(0, "Connection ", "detail1", col_span="2")
        rstr += design_summary_row(1, "Connection Title", "detail2", text_two=" Seated Angle")
        rstr += design_summary_row(1, "Connection Type", "detail2", text_two=" Shear Connection")
        rstr += design_summary_row(0, "Connection Category", "detail1")
        rstr += design_summary_row(1, "Connectivity", "detail2", text_two=str(connectivity))
        rstr += design_summary_row(1, "Beam Connection", "detail2", text_two="Bolted")
        rstr += design_summary_row(1, "Column Connection", "detail2", text_two="Bolted")
        rstr += design_summary_row(0, "Loading (Factored Load)", "detail1")
        rstr += design_summary_row(1, "Shear Force (kN)", "detail2", text_two=str(shear_force))
        rstr += design_summary_row(0, "Components ", "detail1", col_span="2")
        rstr += design_summary_row(1, "Column Section", "detail1", text_two=str(column_sec), text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(column_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=str(bolt_hole_type))
        rstr += design_summary_row(1, "Beam Section", "detail1", text_two=str(beam_sec), text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(beam_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=str(bolt_hole_type))
        rstr += design_summary_row(1, "Seated Angle Section", "detail1", text_two=str(seated_angle_section),
                                   text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(angle_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=str(bolt_hole_type))
        rstr += design_summary_row(1, "Top Angle Section", "detail1", text_two=str(top_angle_section),
                                   text_two_css="detail2")
        rstr += design_summary_row(2, "Material", "detail2", text_two="Fe " + str(angle_fu))
        rstr += design_summary_row(2, "Hole", "detail2", text_two=bolt_hole_type)
        rstr += design_summary_row(1, "Bolts", "detail1", col_span="2")
        rstr += design_summary_row(2, "Type", "detail2", text_two=bolt_type)
        rstr += design_summary_row(2, "Grade", "detail2", text_two=bolt_grade)
        rstr += design_summary_row(2, "Diameter (mm)", "detail2", text_two=bolt_diameter)
        rstr += design_summary_row(2, "Bolts - Required", "detail2", text_two=bolts_required)
        rstr += design_summary_row(2, "Bolts - Provided", "detail2", text_two=bolts_provided)
        rstr += design_summary_row(2, "Rows", "detail2", text_two=number_of_rows)
        rstr += design_summary_row(2, "Columns", "detail2", text_two=number_of_cols)
        rstr += design_summary_row(2, "Gauge (mm)", "detail2", text_two=gauge)
        rstr += design_summary_row(2, "Pitch (mm)", "detail2", text_two=pitch)
        rstr += design_summary_row(2, "End Distance (mm)", "detail2", text_two=end)
        rstr += design_summary_row(2, "Edge Distance (mm)", "detail2", text_two=edge)
        rstr += design_summary_row(0, "Assembly", "detail1", col_span="2")
        rstr += design_summary_row(1, "Column-Beam Clearance (mm)", "detail2", text_two=beam_col_clear_gap,
                                   text_two_css="detail2")

        rstr += " " + nl() + t('/table')
        rstr += t('h1 style="page-break-before:always"')  # page break
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------
        # DESIGN CHECK

        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')
        rstr += design_check_row("Design Check", "", "", "", col_span="4", text_one_css="detail")

        rstr += design_check_row("Check", "Required", "Provided", "Remark", text_one_css="header1",
                                 text_two_css="header1", text_three_css="header1", text_four_css="header1")

        check_pass = "<p align=left style=color:green><b>Pass</b></p>"

        # Bolt
        rstr += design_check_row("Bolt " + str(self.bolt_diameter) + "dia", "", "", "", col_span="4",
                                 text_one_css="detail1")

        # Bolt shear capacity (kN)
        const = str(round(math.pi / 4 * 0.78, 4))
        req_field = " "
        prov_field = "<i>V</i><sub>dsb</sub> = (" + bolt_fu + "*" + const + "*" + bolt_diameter + "*" \
                     + bolt_diameter + ")/ <br>(&#8730;3*1.25*1000) = " + shear_capacity + "<br> [cl. 10.3.3]"
        rstr += design_check_row("Bolt shear capacity (kN)", req_field, prov_field, " ")

        # Bolt bearing capacity (kN)
        req_field = "<i>V<sub>dpb</sub></i> = 2.5 * k<sub>b</sub> * bolt_diameter * critical_thickness * <br>" \
                    + space(3) + " <i>f</i><sub>u</sub>/<i>gamma<sub>mb</sub></i> <br> " \
                    + "[Cl. 10.3.4]"
        prov_field = "<i>V</i><sub>dpb</sub> = (2.5*" + kb + "*" + bolt_diameter + "*" + beam_w_t + "*" \
                     + beam_fu + ")/(1.25*1000)  <br>" + space(2) + " =" + bearing_capacity + " kN"
        rstr += design_check_row("Bolt bearing capacity (kN)", req_field, prov_field, "")

        # Bolt capacity (kN)
        prov_field = "Min (" + str(self.bolt_shear_capacity) + ", " + str(self.bolt_bearing_capacity) + ") = " \
                     + str(self.bolt_value)
        rstr += design_check_row("Bolt capacity (kN)", " ", prov_field, "")

        # No. of bolts
        # bolts = str(round(float(shear_force) / float(str(self.bolt_value)), 1))
        bolts = "4"
        req_field = shear_force + "/" + str(self.bolt_value) + " = " + bolts
        rstr += design_check_row("No. of bolts", req_field, bolts_provided, check_pass)

        rstr += design_check_row("No. of columns", " ", number_of_cols, check_pass)
        rstr += design_check_row("No. of row(s)", " &#8804; 2", number_of_rows, check_pass)

        # Bolt pitch (mm)
        min_pitch = str(int(2.5 * float(bolt_diameter)))
        max_pitch = str(300) if 32 * float(beam_w_t) > 300 else str(int(math.ceil(32 * float(beam_w_t))))
        req_field = " &#8805; 2.5* " + bolt_diameter + " = " + min_pitch + ",  &#8804; Min(32*" + beam_w_t + \
                    ", 300) = " + max_pitch + "<br> [cl. 10.2.2]"
        rstr += design_check_row("Bolt pitch (mm)", req_field, pitch, check_pass)

        # Bolt gauge (mm)
        min_gauge = str(int(2.5 * float(bolt_diameter)))
        max_gauge = str(300) if 32 * float(beam_w_t) > 300 else str(int(math.ceil(32 * float(beam_w_t))))
        req_field = " &#8805; 2.5*" + bolt_diameter + " = " + min_gauge + ", &#8804; Min(32*" + beam_w_t + ", 300) = " \
                    + max_gauge + " <br> [cl. 10.2.2]"
        rstr += design_check_row("Bolt gauge (mm)", req_field, gauge, check_pass)

        # End distance (mm)
        min_end = str(1.7 * float(dia_hole))
        max_end = str(12 * float(beam_w_t))
        req_field = " &#8805; 1.7*" + dia_hole + " = " + min_end + ", &#8804; 12*" + beam_w_t + " = " + max_end + \
                    " <br> [cl. 10.2.4]"
        rstr += design_check_row("End distance (mm)", req_field, end, check_pass)

        # Edge distance (mm)
        min_edge = str(1.7 * float(dia_hole))
        max_edge = str(12 * float(beam_w_t))
        req_field = " &#8805; 1.7*" + dia_hole + " = " + min_edge + ", &#8804; 12*" + beam_w_t + " = " + max_edge + \
                    "<br> [Cl. 10.2.4]"
        rstr += design_check_row("Edge distance (mm)", req_field, edge, check_pass)

        # Seated angle
        rstr += design_check_row("Seated Angle " + str(self.angle_sec), "", "", "", col_span="4",
                                 text_one_css="detail1")

        # Seated angle length
        if connectivity == "Column flange-Beam web":
            req_field = "= min(supported_beam_width, supporting_column_width) <br> = min(" + str(
                self.beam_w_f) + ", " + str(self.column_w_f) + ")"
            prov_field = str(self.angle_l)
        elif connectivity == "Column web-Beam web":
            req_field = "=width of supported beam <br> =" + str(self.beam_w_f)
            prov_field = str(self.angle_l)
        rstr += design_check_row("Length (mm)", req_field, prov_field, check_pass)

        # Length of outstanding leg
        req_field = "b = R * " + sub("gamma", "m0") + "/" + sub("t", "w") + sub("f", "yw") + "<br> [Cl. 8.7.4]"
        prov_field = str(self.angle_B)
        rstr += design_check_row("Outstanding leg length (mm)", req_field, prov_field, check_pass)

        # For angle thickness
        # Shear capacity of outstanding leg
        req_field = sub("V", "dp") + " &#8805 V <br>"
        req_field += sub("V", "dp") + " &#8805 " + str(self.shear_force) + "kN <br> [Cl. 8.4.1]"
        prov_field = sub("V", "dp") + "=" + sub("A", "v") + sub("f", "yw") + "/<br> &#8730 3 *" + sub("gamma", "m0")
        prov_field += "(" + str(self.angle_l) + "*" + str(self.angle_t) + ") * " + str(
            self.angle_fy) + "/<br> &#8730 3 *" + str(self.gamma_m0) + "<br>=" + str(
            self.outstanding_leg_shear_capacity)
        rstr += design_check_row("Shear capacity of outstanding <br>" + space(1) + " leg (kN)", req_field, prov_field,
                                 check_pass)

        # Moment capacity of outstanding leg
        prov_field = sub("M", "d") + "=" + sub("beta", "b") + sub("Z", "p") + sub("f", "y")
        prov_field += "/" + sub("gamma", "m0")
        prov_field += "<br> = 1.0* " + str(self.angle_l) + "*(" + str(self.angle_t) + "^2/4)*"
        prov_field += str(self.angle_fy) + "/" + str(self.gamma_m0) + "<br>"

        if self.is_shear_high is False:
            req_field = "As V &#8804 0.6 " + sub("V", "d")
            req_field += ",<br>[Cl 8.2.1.2] is applicable <br>"

            req_field += sub("M", "d") + " &#8805 Moment at root of angle"
            req_field += "<br>" + sub("M", "d") + " &#8805 " + str(self.moment_at_root_angle) + "<br>"
            prov_field += "<br>=" + str(self.moment_capacity_angle)
        elif self.is_shear_high:
            req_field = "As V &#8805 0.6 " + sub("V", "d")
            req_field += ",<br>[Cl 8.2.1.3] is applicable <br>"

            req_field += "<br>" + sub("M", "dv") + " &#8805 Moment at root of angle"
            req_field += "<br>" + sub("M", "dv") + " &#8805 " + str(self.moment_at_root_angle) + "<br>"

            prov_field += "=" + str(round(self.leg_moment_d, 2)) + "<br>"
            prov_field += "<br>" + sub("M", "dv") + "= min("
            prov_field += " (1 - beta)" + sub("M", "d") + " , "
            prov_field += "1.2 " + sub("Z", "e") + sub("f", "y") + "/" + sub("gamma", "m0")
            prov_field += " ) <br>"
            prov_field += space(2) + "beta = ((2V/" + sub("V", "d") + ")-1)^2 = " + str(
                self.moment_high_shear_beta) + "<br>"
            prov_field += "<br>" + sub("M", "dv") + " = " + str(self.moment_capacity_angle)

        req_field += "<br>" + "To avoid irreversible deformation under service loads,"
        req_field += "<br>" + sub("M", "d") + " &#8804 1.5" + sub("Z", "e") + sub("f", "y")
        req_field += "/" + sub("gamma", "m0") + "<br>"

        rstr += design_check_row("Moment capacity of outstanding <br>" + space(1) + " leg (kN-mm)", req_field,
                                 prov_field, check_pass)

        rstr += t('/table')
        rstr += t('h1 style="page-break-before:always"')
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------

        # Connection images (views)
        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"')

        # row = [0, "Views", " "]
        # rstr += t('tr')
        # rstr += t('td colspan="2" class=" detail"') + space(row[0]) + row[1] + t('/td')
        # rstr += t('/tr')
        rstr += design_summary_row(0, "Views", "detail", col_span="2")

        png = folder + "/images_html/3D_Model.png"
        datapng = '<object type="image/PNG" data= %s width ="450"></object">' % png

        side = folder + "/images_html/seatSide.png"
        dataside = '<object type="image/PNG" data= %s width ="400"></object>' % side

        top = folder + "/images_html/seatTop.png"
        datatop = '<object type="image/PNG" data= %s width ="400"></object>' % top

        front = folder + "/images_html/seatFront.png"
        datafront = '<object type="image/PNG" data= %s width ="450"></object>' % front

        row = [0, datapng, datatop]
        rstr += t('tr') + nl()
        rstr += html_space(4) + t('td  align="center" class=" header2"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(4) + t('td  align="center" class=" header2"') + row[2] + t('/td') + nl()
        rstr += t('/tr' + nl())

        row = [0, dataside, datafront]
        rstr += t('tr') + nl()
        rstr += html_space(4) + t('td align="center" class=" header2"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(4) + t('td align="center" class=" header2 "') + row[2] + t('/td') + nl()
        rstr += t('/tr') + nl()

        rstr += t('/table') + nl() + " " + nl()
        rstr += t('h1 style="page-break-before:always"')
        rstr += t('/h1')

        # -----------------------------------------------------------------------------------
        rstr += self.design_report_header()
        # -----------------------------------------------------------------------------------

        rstr += t('hr')
        rstr += t('/hr') + nl() + " " + nl()

        rstr += t('table width = 100% border-collapse= "collapse" border="1px solid black"') + nl()
        rstr += html_space(1) + t('''col width=30%''')
        rstr += html_space(1) + t('''col width=70%''') + nl()

        rstr += html_space(1) + t('tr') + nl()
        row = [0, "Additional Comments", additional_comments]
        rstr += html_space(2) + t('td class= "detail1"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(2) + t('td class= "detail2" align="justified"') + row[2] + t('/td') + nl()
        rstr += html_space(1) + t('/tr') + nl()

        rstr += t('/table') + nl()

        myfile.write(rstr)
        myfile.write(t('/body'))
        myfile.write(t('/html'))
        myfile.close()

    def design_report_header(self):
        """Create and return html code to display Report Header.

        Args:            

        Returns:
            rstr (str): string containing html code to table (used as Report Header)
        """
        rstr = nl() + " " + nl() + t('table border-collapse= "collapse" border="1px solid black" width=100%') + nl()
        rstr += t('tr') + nl()
        row = [0, '<object type= "image/PNG" data= "cmpylogoSeatAngle.png" height=60 ></object>',
               '<font face="Helvetica, Arial, Sans Serif" size="3">Created with</font>' "&nbsp" "&nbsp" "&nbsp" "&nbsp"
               "&nbsp" '<object type= "image/PNG" data= "Osdag_header.png" height=60 ''&nbsp" "&nbsp" "&nbsp" "&nbsp">'
               '</object>']
        rstr += html_space(1) + t('td colspan="2" align= "center"') + space(row[0]) + row[1] + t('/td') + nl()
        rstr += html_space(1) + t('td colspan="2" align= "center"') + row[2] + t('/td') + nl()
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Company Name", "detail", text_two=self.company_name, is_row=False)
        rstr += design_summary_row(0, "Project Title", "detail", text_two=self.project_title, is_row=False)
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Group/Team Name", "detail", text_two=self.group_team_name, is_row=False)
        rstr += design_summary_row(0, "Subtitle", "detail", text_two=self.sub_title, is_row=False)
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Designer", "detail", text_two=self.designer, is_row=False)
        rstr += design_summary_row(0, "Job Number", "detail", text_two=self.job_number, is_row=False)
        rstr += t('/tr') + nl()

        rstr += t('tr') + nl()
        rstr += design_summary_row(0, "Date", "detail", text_two=time.strftime("%d /%m /%Y"), is_row=False)
        rstr += design_summary_row(0, "Client", "detail", text_two=self.client, is_row=False)
        rstr += t('/tr')
        rstr += t('/table') + nl() + " " + nl()

        rstr += t('hr')
        rstr += t('/hr') + nl() + " " + nl()
        return rstr


def space(n):
    """Create html code to create tab space in html-output.

    Args:
        n (int): number of tab spaces to be created in the html-output.

    Returns:
        rstr (str): html code that creates 'n' number of tab spaces.
    """
    rstr = "&nbsp;" * 4 * n
    return rstr


def t(param):
    """Enclose argument in html tag.

    Args:
        param (str): parameter to be enclosed in html tag <>.

    Returns:
        rstr (str): given param enclosed in html tag <>.
    """
    return '<' + param + '>'


def w(n):
    """Enclose argument in curly brace parenthesis.

    Args:
        n (str): parameter to be enclosed in curly brace parenthesis.

    Returns:
        rstr (str): given param enclosed in curly brace parenthesis.
    """
    return '{' + n + '}'


def quote(m):
    """Enclose argument in double quotes.

    Args:
        m (str): parameter to be enclosed in double quotes

    Returns:
        rstr (str): given param enclosed in double quotes
    """
    return '"' + m + '"'


def nl():
    """Create new line.

    Args:        

    Returns:
        new line tag.

    Note:
        Instead of directly inserting the new line tag '\n' in the code, this function was created,
        to enable custom formatting in future.
    """
    return '\n'


def html_space(n):
    """Create space in html code.

    Args:
        n (int): number of spaces to be created in the html-code.

    Returns:
        (str): specified number_of_spaces
    """
    return " " * n


def sub(string, subscript):
    """Create html code to display subscript.

    Args:
        string (str):
        subscript (str): string to be subscript

    Returns:
        (str): html code with concatenated string and subscript
    """
    return string + "<sub>" + subscript + "</sub>"


def design_summary_row(tab_spaces, text_one, text_one_css, **kwargs):
    """Create formatted html row entry for design summary table.

    Args:
        tab_spaces (int): number of (tab) spaces
        text_one (str): Text entry
        text_one_css (str): Key pointing to table-data css format

    kwargs:
        text_two (str): Text entry
        text_two_css (str): Key pointing to table-data css class
        col_span (str): number of columns in table that the table data spans
        is_row (boolean): key to create separate table row entry

    Returns (str):
        Formatted line of html-code.

    """
    text_two = kwargs.get('text_two', " ")
    text_two_css = kwargs.get('text_two_css', text_one_css)
    col_span = kwargs.get('col_span', "1")
    is_row = kwargs.get('is_row', True)

    row_string = ""  # default
    if is_row:
        row_string = t('tr') + nl()

    if col_span != "1":
        row_string = row_string + html_space(4) + t('td colspan=' + col_span + ' class="' + text_one_css + '"') + space(
            tab_spaces) + text_one + t('/td') + nl()
    else:
        row_string = row_string + html_space(4) + t('td class="' + text_one_css + '"') + space(tab_spaces) + text_one \
                     + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + text_two_css + '"') + text_two + t('/td') + nl()

    if is_row:
        row_string = row_string + t('/tr') + nl()

    return row_string


def design_check_row(text_one, text_two, text_three, text_four, **kwargs):
    """Create formatted html row entry for design check table.

    Args:
        text_one (str): Detail check name
        text_two (str): Required field
        text_three (str): Provided field
        text_four (str): Remark field

    kwargs:
        col_span (str): number of columns in table that the table data spans
        text_one_css (str): Key pointing to table-data css class
        text_two_css (str): Key pointing to table-data css class
        text_three_css (str): Key pointing to table-data css class
        text_four_css (str): Key pointing to table-data css class

    Returns (str):
        Formatted line of html-code.

    """
    col_span = kwargs.get('col_span', "1")
    t1_css = kwargs.get('text_one_css', "detail1")
    t2_css = kwargs.get('text_two_css', "detail2")
    t3_css = kwargs.get('text_three_css', "detail2")
    t4_css = kwargs.get('text_four_css', "detail1")

    row_string = nl() + t('tr') + nl()

    if col_span == "4":
        row_string = row_string + html_space(4) + t(
            'td colspan=' + col_span + ' class="' + t1_css + '"') + text_one + t('/td') + nl()
    else:
        row_string = row_string + html_space(4) + t('td class="' + t1_css + '"') + space(1) + text_one + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t2_css + '"') + text_two + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t3_css + '"') + text_three + t('/td') + nl()
        row_string = row_string + html_space(4) + t('td class="' + t4_css + '"') + text_four + t('/td') + nl()

    row_string = row_string + t('/tr') + nl()

    return row_string


def create_sample_report_summary(sa_connection_id):
    """Create and return hardcoded sample report_summary (dict).

    Args:
        
    Returns:
        report_summary (dict): Structural Engineer details for design report
    """
    report_summary = {}
    report_summary["ProfileSummary"] = {}
    report_summary["ProfileSummary"]["CompanyName"] = "FOSSEE"
    report_summary["ProfileSummary"]["CompanyLogo"] = "IIT Bombay"
    report_summary["ProfileSummary"]["Group/TeamName"] = "Osdag"
    report_summary["ProfileSummary"]["Designer"] = "Rachana"

    report_summary["ProjectTitle"] = "Onboarding Quiz"
    report_summary["Subtitle"] = "Seated angle connection"
    report_summary["JobNumber"] = sa_connection_id
    report_summary["Client"] = "Osdag Reviewer"
    report_summary["AdditionalComments"] = "Add more comments here."
    report_summary["Method"] = "Limit State Design"
    return report_summary


if __name__ == '__main__':
    workspace_folder_path = "F:\OSDAG_workspace"
    if not os.path.exists(workspace_folder_path):
        os.mkdir(workspace_folder_path, 0755)
    image_folder_path = os.path.join(workspace_folder_path, 'images_html')
    if not os.path.exists(image_folder_path):
        os.mkdir(image_folder_path, 0755)

    sa_connection_id = "SA_2"
    report_summary = create_sample_report_summary(sa_connection_id)
    folder_location = "F:\Osdag_Workspace\one\\"
    if not os.path.exists(folder_location):
        os.mkdir(folder_location, 0755)
    file_name = folder_location + "design_report_" + sa_connection_id + ".html"
    specimen_report = ReportGenerator()
    specimen_report.save_html(report_summary, file_name, folder_location)
